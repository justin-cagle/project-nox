"""
Pydantic schemas related to authentication tokens.

These schemas define token metadata structures used during email verification
and token tracking (e.g. replay prevention).
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UsedToken(BaseModel):
    """
    Schema representing a used token (for anti-reuse).

    Attributes:
        id (UUID): Primary ID of the token record.
        user_id (UUID): ID of the user this token was issued to.
        token_hash (str): Hashed version of the token string.
        issued_at (datetime): Timestamp when the token was issued.
        created_at (datetime): Timestamp when the token was stored as used.
    """

    id: UUID
    user_id: UUID
    token_hash: str
    issued_at: datetime
    created_at: datetime


class VerifyEmailToken(BaseModel):
    """
    Schema for email verification request parameters.

    Attributes:
        token (str): The raw JWT provided in the query string.
    """

    token: str
