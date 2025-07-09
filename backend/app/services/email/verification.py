from fastapi_mail import MessageSchema, MessageType

from app.core.config import settings
from app.core.email_client import get_email_client
from app.core.tokens.email import get_email_token
from app.services.email.template import render_dual_template


async def send_verification_email(user: dict) -> None:
    token = get_email_token(user_id=user["user_id"])

    context = {
        "display_name": user.get("display_name"),
        "email": user.get("email"),
        "verification_url": f"{settings.CLIENT_ORIGIN}/verify-email?token={token}",
    }

    html_body, text_body = render_dual_template("verification", context)

    message = MessageSchema(
        subject="Confirm your email for Project Nox",
        recipients=[user["email"]],
        body=html_body or text_body,  # Prefer HTML if present
        subtype=MessageType.html if html_body else MessageType.plain,
    )

    mailer = get_email_client()
    await mailer.send_message(message)
