"""
API v1 base routes for authentication.

This module defines the primary authentication routes for user registration
and email verification. It leverages FastAPI's dependency injection system and
custom token validation logic.
"""

from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.core.tokens.base import validate_token
from app.core.tokens.purposes import TokenPurpose
from app.exceptions.handlers import TokenValidationError
from app.schemas.auth import VerifyEmailToken
from app.schemas.user import UserCreate
from app.services.user import create_user

router = APIRouter()


@router.post("/auth/register")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user and sends a verification email.

    Args:
        user_in (UserCreate): The input user registration data.
        db (AsyncSession): Database session injected by FastAPI.

    Returns:
        dict: A message confirming registration and whether email verification is required.
    """
    # Create the user in the database and trigger any related logic (e.g., sending verification).
    user = await create_user(user_in, db)
    return {
        "message": "Registration successful. Verification email sent.",
        "userId": user.id,
        "emailVerificationRequired": True,
    }


@router.get("/auth/verify")
async def verify_email(
    query: VerifyEmailToken = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Verifies a user's email by validating their token.

    Args:
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
        # TODO: Clarify expected behavior on token failure — is this user-facing?
        return JSONResponse(
            status_code=400,
            content={"message": str(e)},
        )

    # Email verification successful.
    return {"message": "Email verified successfully.", "userId": user_id}
