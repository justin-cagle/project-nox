from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.dialects.postgresql.base import UUID

from app.exceptions.handlers import TokenValidationError


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
