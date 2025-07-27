"""
JWT token utilities for authentication and verification.

This module provides functions to create, decode, and validate purpose-bound
JWTs. It includes database-backed protection against token reuse via the
`UsedToken` model and enforces strict decoding + purpose checking.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_str
from app.core.tokens.purposes import TokenPurpose
from app.core.tokens.status import TokenStatus
from app.exceptions.handlers import TokenValidationError
from app.models import User
from app.models.used_token import UsedToken


def create_token(
    user_id: UUID, purpose: str, expires_delta: timedelta, secret: str
) -> str:
    """
    Creates a signed JWT for a given user and purpose.

    Args:
        user_id (UUID): ID of the user the token is for.
        purpose (str): The intended use of the token (e.g., 'verify_email').
        expires_delta (timedelta): How long the token should be valid.
        secret (str): Secret used to sign the JWT.

    Returns:
        str: The encoded JWT.
    """
    exp = datetime.now(tz=timezone.utc) + expires_delta
    return jwt.encode(
        {"sub": str(user_id), "exp": exp, "purpose": purpose}, secret, algorithm="HS256"
    )


def decode_token(token: str, expected_purpose: str, secret: str) -> dict:
    """
    Decodes a JWT and validates its intended purpose.

    Args:
        token (str): JWT string to decode.
        expected_purpose (str): Purpose expected to be embedded in the token.
        secret (str): Secret key used to decode and verify the token.

    Returns:
        dict: Decoded payload of the token.

    Raises:
        TokenValidationError: If decoding fails or the purpose is incorrect.
    """
    try:
        dec = jwt.decode(token, secret, algorithms=["HS256"])
    except JWTError:
        raise TokenValidationError("JWT decode failed")

    if dec.get("purpose") != expected_purpose:
        raise TokenValidationError(f"Unexpected token purpose: {dec.get('purpose')}")

    unix_time = datetime.fromtimestamp(dec.get("exp"), tz=timezone.utc)

    if unix_time <= datetime.now(tz=timezone.utc):
        raise TokenValidationError("Token has expired")

    return dec


async def validate_token(
    token: str, purpose: str, secret: str, db: AsyncSession
) -> UUID:
    """
    Validates a JWT and checks it hasn't been reused.

    Args:
        token (str): The JWT string.
        purpose (str): Expected token purpose (e.g., 'verify_email').
        secret (str): Secret for decoding the token.
        db (AsyncSession): Async SQLAlchemy session for DB checks.

    Returns:
        UUID: The `sub` (user ID) field from the token.

    Raises:
        TokenValidationError: If the token is invalid, expired, reused, or purpose mismatched.
    """
    try:
        payload = decode_token(token, purpose, secret)
    except TokenValidationError:
        raise TokenValidationError("Token could not be decoded")

    try:
        raw_sub = payload.get("sub")
        user_id = raw_sub if isinstance(raw_sub, UUID) else UUID(raw_sub)
    except (TypeError, ValueError):
        raise TokenValidationError("Token subject is invalid or missing")

    token_hash = hash_str(token, purpose)

    result = await db.execute(select(UsedToken).filter_by(token_hash=token_hash))
    entry = result.scalar_one_or_none()

    if not entry:
        raise TokenValidationError("Token not found or already used")
    if (
        entry.status != TokenStatus.ISSUED
        or entry.purpose != TokenPurpose.EMAIL_VERIFICATION
        or entry.redeemed_at is not None
    ):
        raise TokenValidationError("Token expired or invalid")

    return user_id


async def modify_token_status(token: str, purpose: str, db: AsyncSession) -> None:
    token_hash = hash_str(token, purpose)

    try:
        stmt = select(UsedToken).where(UsedToken.token_hash == token_hash)
        result = await db.execute(stmt)
        used_token = result.scalar_one_or_none()

        if not used_token:
            raise TokenValidationError("Token not found")

        used_token.status = TokenStatus.REDEEMED
        used_token.redeemed_at = datetime.now(tz=timezone.utc)

        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error")
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error")


async def mark_user_verified(user_id: UUID, db: AsyncSession) -> None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    user.verified_at = datetime.now(tz=timezone.utc)  # Optional

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Could not verify user")
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
