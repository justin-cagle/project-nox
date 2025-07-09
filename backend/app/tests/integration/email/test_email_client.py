import pytest
from fastapi_mail import MessageSchema, MessageType

from app.core.email_client import get_email_client


@pytest.mark.asyncio
@pytest.mark.skip(reason="Manual integration test for email delivery")
async def test_send_email():
    message = MessageSchema(
        subject="Test Email from Project Nox",
        recipients=["email@address.com"],  # Replace with your email for test
        body="This is a test email from the integration test suite.",
        subtype=MessageType.plain,
    )

    mailer = get_email_client()
    await mailer.send_message(message)
