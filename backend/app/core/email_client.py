"""
Email client singleton using FastAPI-Mail.

Provides a global `FastMail` instance based on settings,
configured on-demand to send outbound emails.
"""

from fastapi_mail import ConnectionConfig, FastMail

from app.core.config import settings as s

# Global client cache (lazy-loaded)
_email_client = None


def get_email_client() -> FastMail:
    """
    Lazily initialize and return a global FastMail instance.

    Uses application settings to configure SMTP transport.
    Subsequent calls return the cached instance.

    Returns:
        FastMail: A configured FastAPI-Mail client.
    """
    global _email_client
    if _email_client is None:
        _email_client = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=s.EMAIL_USERNAME,
                MAIL_PASSWORD=s.EMAIL_PASSWORD,
                MAIL_PORT=s.EMAIL_PORT,
                MAIL_SERVER=s.EMAIL_SERVER,
                MAIL_STARTTLS=s.EMAIL_USE_TLS,
                MAIL_FROM=s.EMAIL_FROM,
                MAIL_FROM_NAME=s.EMAIL_FROM_NAME,
                MAIL_SSL_TLS=s.EMAIL_USE_SSL,
                MAIL_DEBUG=True,
            )
        )
    return _email_client


def reset_email_client() -> None:
    """
    Reset the cached FastMail instance.

    Primarily used in test environments to reconfigure or isolate state.
    """
    global _email_client
    _email_client = None
