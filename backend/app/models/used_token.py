"""
SQLAlchemy model definition for `UsedToken`.

Tracks the lifecycle and usage of hashed tokens, such as:
- One-time email verification links
- Password reset tokens
- Any token with single-use or revocation semantics
"""

import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from app.core.base import Base


class UsedToken(Base):
    """
    ORM model for storing metadata about previously used or issued tokens.

    Fields:
        id (UUID): Unique record identifier.
        token_hash (str): Hashed representation of the original token. Indexed for lookup.
        purpose (str): Human-readable description of the token's intent (e.g., "email_verification").
        created_at (datetime): Timestamp when the token was issued/stored.
        redeemed_at (datetime | None): Optional timestamp for when the token was used or consumed.
        status (str): Freeform status label (e.g., "used", "revoked", "expired").
    """

    __tablename__ = "used_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Hashed form of the token; never store raw token data
    token_hash = Column(String, nullable=False, index=True)

    # Optional purpose tag (e.g. "password_reset")
    purpose = Column(String)

    # Created automatically at insert
    created_at = Column(DateTime, default=func.now())

    # Set to non-null when the token is consumed
    redeemed_at = Column(DateTime, nullable=True)

    # Status field for audit/debugging (e.g. used/revoked/expired)
    status = Column(String)
