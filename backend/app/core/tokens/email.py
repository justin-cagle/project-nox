from datetime import timedelta

from purposes import TokenPurpose
from sqlalchemy.dialects.postgresql.base import UUID

from app.core.config import settings
from app.core.tokens.base import create_token


def get_email_token(user_id: UUID) -> str:
    return create_token(
        user_id,
        TokenPurpose.EMAIL_VERIFICATION,
        timedelta(minutes=settings.EMAIL_TOKEN_EXPIRES_MINUTES),
        settings.EMAIL_TOKEN_SECRET,
    )
