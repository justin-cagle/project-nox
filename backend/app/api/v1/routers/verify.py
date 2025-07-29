from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.messages import Errors, Verification
from app.core.config import settings
from app.core.db import get_db
from app.core.limiting import limiter
from app.core.tokens.base import mark_user_verified, modify_token_status, validate_token
from app.core.tokens.purposes import TokenPurpose
from app.exceptions.handlers import TokenValidationError
from app.schemas.auth import VerifyEmailToken
from app.services.onboarding import onboard_after_user_created
from app.services.user import get_user_by_email, get_user_by_username

router = APIRouter()


@router.get("/verify")
@limiter.limit("3/minute")
async def verify_email(
    request: Request,
    query: VerifyEmailToken = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        user_id = await validate_token(
            token=query.token,
            purpose=TokenPurpose.EMAIL_VERIFICATION,
            secret=settings.EMAIL_TOKEN_SECRET,
            db=db,
        )
    except TokenValidationError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    try:
        await modify_token_status(
            token=query.token,
            purpose=TokenPurpose.EMAIL_VERIFICATION,
            db=db,
        )
        await mark_user_verified(user_id=user_id, db=db)
    except HTTPException as e:
        raise e

    return {"message": Verification.SUCCESS, "userId": user_id}


@router.post("/verify/resend")
@limiter.limit("2/minute")
async def resend_verification_email(
    request: Request,
    username: str = None,
    email: str = None,
    db: AsyncSession = Depends(get_db),
):
    if email:
        user = await get_user_by_email(email, db)
    elif username:
        user = await get_user_by_username(username, db)
    else:
        raise HTTPException(status_code=400, detail=Errors.GENERIC)

    if user:
        try:
            await onboard_after_user_created(user, db)
        except Exception:
            pass

    return {"message": "If the account exists, a verification email was sent."}
