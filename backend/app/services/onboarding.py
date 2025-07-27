from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.messages import Errors, Registration
from app.core.tokens.email import get_email_token
from app.core.tokens.purposes import TokenPurpose
from app.core.tokens.status import TokenStatus
from app.models import User
from app.schemas.user import UserCreate
from app.services.email.verification import (
    insert_token,
    mark_token_as_issued,
    send_verification_email,
)
from app.services.user import create_user


async def onboard_user(user_in: UserCreate, db: AsyncSession) -> dict[str, str] | None:
    try:
        user = await create_user(user_in, db)
    except HTTPException as e:
        raise e

    return await onboard_after_user_created(user, db)


async def onboard_after_user_created(user: User, db: AsyncSession) -> dict[str, str]:
    email_token = get_email_token(user_id=user.id)

    try:
        result = await insert_token(
            user_id=user.id,
            purpose=TokenPurpose.EMAIL_VERIFICATION,
            token=email_token,
            status=TokenStatus.PENDING,
            db=db,
        )
    except HTTPException as r:
        return {"success": False, "message": Errors.GENERIC, "detail": str(r)}

    try:
        await send_verification_email(user=user, token=email_token)
    except Exception as f:
        return {"success": False, "message": Errors.GENERIC, "detail": str(f)}

    try:
        await mark_token_as_issued(user_id=user.id, token=email_token, db=db)
    except HTTPException as e:
        return {"success": False, "message": Errors.GENERIC, "detail": str(e)}

    return {"success": True, "message": Registration.SUCCESS, "user_id": str(user.id)}
