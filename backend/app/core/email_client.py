from fastapi_mail import ConnectionConfig, FastMail

from app.core.config import settings as s

_email_client = None


def get_email_client() -> FastMail:
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
    global _email_client
    _email_client = None
