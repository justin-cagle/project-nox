"""
JWT token utilities for authentication and verification.

This module provides functions to create, decode, and validate purpose-bound
JWTs. It includes database-backed protection against token reuse via the
`UsedToken` model and enforces strict decoding + purpose checking.
"""

from datetime import datetime, timedelta, timezone
from http.client import HTTPException

from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_str
from app.exceptions.handlers import TokenValidationError
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

    # Extract and normalize fields from the decoded payload.
    user_id = payload.get("sub")
    if user_id is None:
        raise TokenValidationError("Token missing subject")

    token_hash = hash_str(token)

    # Check whether the token has already been used (replay protection).
    result = await db.execute(select(UsedToken).filter_by(token_hash=token_hash))
    if result.scalar_one_or_none():
        raise TokenValidationError("Token has already been used")

    # Mark this token as used to prevent future replays.
    db.add(UsedToken(token_hash=token_hash))
    await db.commit()

    return user_id
