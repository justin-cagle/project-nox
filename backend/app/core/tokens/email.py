"""
Email verification token generator.

Creates purpose-bound, time-limited tokens tied to user identity,
specifically for email verification workflows.
"""

from datetime import timedelta

from sqlalchemy.dialects.postgresql.base import UUID

from app.core.config import settings
from app.core.tokens.base import create_token
from app.core.tokens.purposes import TokenPurpose


def get_email_token(user_id: UUID) -> str:
    """
    Generate a short-lived token for verifying the user's email address.

    Args:
        user_id (UUID): Unique identifier for the target user.

    Returns:
        str: Signed and encoded verification token.
    """
    return create_token(
        user_id,
        TokenPurpose.EMAIL_VERIFICATION,
        timedelta(minutes=settings.EMAIL_TOKEN_EXPIRES_MINUTES),
        settings.EMAIL_TOKEN_SECRET,
        version=None,
    )
