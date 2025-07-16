from uuid import UUID

from fastapi import HTTPException
from fastapi_mail import MessageSchema, MessageType
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.constants.messages import Errors
from app.core.config import settings
from app.core.email_client import get_email_client
from app.core.security import hash_str
from app.core.tokens.purposes import TokenPurpose
from app.core.tokens.status import TokenStatus
from app.models.used_token import UsedToken
from app.models.user import User
from app.services.email.template import render_dual_template


async def send_verification_email(user: User, token: str) -> None:
    context = {
        "display_name": user.display_name,
        "email": user.email,
        "verification_url": f"{settings.CLIENT_ORIGIN}/verify-email?token={token}",
    }

    html_body, text_body = render_dual_template("verification", context)

    message = MessageSchema(
        subject="Confirm your email for Project Nox",
        recipients=[user.email],
        body=html_body or text_body,  # Prefer HTML if present
        subtype=MessageType.html if html_body else MessageType.plain,
    )

    mailer = get_email_client()
    await mailer.send_message(message)


async def insert_token(
    user_id: UUID,
    purpose: TokenPurpose,
    token: str,
    status: TokenStatus,
    db: AsyncSession,
) -> None:
    hashed_token = hash_str(token, purpose)

    entry = UsedToken(
        user_id=user_id,
        token_hash=hashed_token,
        purpose=purpose,
        redeemed_at=None,
        status=status,
    )

    db.add(entry)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail=Errors.DBCOMMIT)
    except SQLAlchemyError:
        # Roll back on any unexpected DB error.
        await db.rollback()
        raise

    await db.refresh(entry)


async def mark_token_as_issued(user_id: UUID, token: str, db: AsyncSession) -> None:
    hashed_token = hash_str(token, TokenPurpose.EMAIL_VERIFICATION)

    result = await db.execute(
        select(UsedToken).where(
            UsedToken.user_id == user_id, UsedToken.token_hash == hashed_token
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=400, detail=Errors.BAD_TOKEN)

    entry.status = TokenStatus.ISSUED

    db.add(entry)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail=Errors.DBCOMMIT)
    except SQLAlchemyError:
        # Roll back on any unexpected DB error.
        await db.rollback()
        raise

    await db.refresh(entry)
