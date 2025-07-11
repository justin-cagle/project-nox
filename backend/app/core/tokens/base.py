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
    exp = datetime.now(tz=timezone.utc) + expires_delta
    return jwt.encode(
        {"sub": str(user_id), "exp": exp, "purpose": purpose}, secret, algorithm="HS256"
    )


def decode_token(token: str, expected_purpose: str, secret: str) -> dict:
    try:
        dec = jwt.decode(token, secret, algorithms=["HS256"])
    except JWTError:
        raise TokenValidationError("JWT decode failed")

    if dec.get("purpose") != expected_purpose:
        raise TokenValidationError(f"Unexpected token purpose: {dec.get('purpose')}")

    return dec


async def validate_token(token: str, purpose: str, secret: str, db: AsyncSession) -> UUID:
    try:
        payload = decode_token(token, purpose, secret)
    except TokenValidationError:
        raise TokenValidationError("Token could not be decoded")

    exp = payload.get("exp")
    user_id = payload.get("sub")
    token_purpose = payload.get("purpose")

    if not user_id or not exp or not token_purpose:
        raise TokenValidationError("Token is missing required fields")

    if datetime.now(tz=timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
        raise TokenValidationError("Token has expired")

    if token_purpose != purpose:
        raise TokenValidationError("Token purpose mismatch")

    hashed = hash_str(token, purpose)
    stmt = select(UsedToken).where(UsedToken.token_hash == hashed)
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()

    if entry is None:
        raise TokenValidationError("Token was not issued by this system")

    if entry.status == "used":
        raise TokenValidationError("Token has already been used")

    return UUID(user_id)
