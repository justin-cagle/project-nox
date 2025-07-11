"""
SQLAlchemy model definition for the `User` table.

Defines a basic user entity with required identity and authentication fields.
"""

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.base import Base


class User(Base):
    """
    SQLAlchemy ORM model for a registered user.

    Attributes:
        id (UUID): Primary key, auto-generated using uuid4.
        username (str): Unique username, indexed for fast lookup.
        email (str): Unique email address, also indexed.
        display_name (str): User-friendly name for display purposes.
        hashed_password (str): Hashed password, never stored in plain text.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUIDv4 PK
    username = Column(String, unique=True, index=True)  # Used for login/display
    email = Column(String, unique=True, index=True)  # Must be validated and unique
    display_name = Column(String)  # Non-unique, user-facing alias
    hashed_password = Column(String, nullable=False)  # Argon2id-hashed login secret
