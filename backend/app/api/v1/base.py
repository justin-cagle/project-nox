"""
API v1 base routes for authentication.

This module defines the primary authentication routes for user registration
and email verification. It leverages FastAPI's dependency injection system and
custom token validation logic.
"""

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
from app.schemas.user import UserCreate
from app.services.onboarding import onboard_after_user_created, onboard_user
from app.services.user import get_user_by_email, get_user_by_username

router = APIRouter()


@router.post("/auth/register")
@limiter.limit("3/minute")
async def register_user(
    request: Request, user_in: UserCreate, db: AsyncSession = Depends(get_db)
):
    """
    Registers a new user and sends a verification email.

    Args:
        request: Needed for slowapi rate-limiting.
        user_in (UserCreate): The input user registration data.
        db (AsyncSession): Database session injected by FastAPI.

    Returns:
        dict: A message confirming registration and whether email verification is required.
    """
    # Create the user in the database and trigger any related logic (e.g., sending verification).
    try:
        result = await onboard_user(user_in=user_in, db=db)
    except HTTPException as e:
        raise e  # Let FastAPI handle it properly

    if not result.get("success"):
        raise HTTPException(
            status_code=409, detail=result.get("detail", "Registration failed")
        )

    return {
        "message": "Registration successful. Verification email sent.",
        "userId": result["user_id"],
        "emailVerificationRequired": True,
    }


@router.get("/auth/verify")
@limiter.limit("3/minute")
async def verify_email(
    request: Request,
    query: VerifyEmailToken = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Verifies a user's email by validating their token.

    Args:
        request: needed for rate limiter
        query (VerifyEmailToken): Token extracted from query parameters.
        db (AsyncSession): Database session.

    Returns:
        JSONResponse: Success response if token is valid, or error message if invalid.
    """
    try:
        # Attempt to validate the token for the correct purpose using app secrets and DB state.
        user_id = await validate_token(
            token=query.token,
            purpose=TokenPurpose.EMAIL_VERIFICATION,
            secret=settings.EMAIL_TOKEN_SECRET,
            db=db,
        )
    except TokenValidationError as e:
        return JSONResponse(
            status_code=400,
            content={"message": str(e)},
        )

    try:
        await modify_token_status(
            token=query.token, purpose=TokenPurpose.EMAIL_VERIFICATION, db=db
        )
    except HTTPException as e:
        raise e

    try:
        await mark_user_verified(user_id=user_id, db=db)
    except HTTPException as e:
        raise e

    # Email verification successful.
    return {"message": Verification.SUCCESS, "userId": user_id}


@router.post("/auth/verify/resend")
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


@router.get("/health")
@limiter.limit("5/minute")
async def get_heartbeat(request: Request):
    return JSONResponse(status_code=200, content={"message": "OK"})
