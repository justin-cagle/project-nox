"""
Manual integration test for email delivery.

⚠️ This test is disabled by default and intended for developers to verify
SMTP credentials and outbound delivery manually. Requires modifying the
recipient email address before execution.

Uses FastAPI-Mail for message construction and async sending.
"""

import pytest
from fastapi_mail import MessageSchema, MessageType

from app.core.email_client import get_email_client


@pytest.mark.asyncio
@pytest.mark.skip(reason="Manual integration test for email delivery")
async def test_send_email():
    """
    Sends a manual test email using the configured mail client.

    To run:
        - Replace `recipients` with a real inbox you control
        - Unskip the test (`@pytest.mark.skip`)
        - Run with: `pytest -k test_send_email`

    Asserts:
        - No exception is raised
        - Email is sent successfully (check inbox manually)
    """
    message = MessageSchema(
        subject="Test Email from Project Nox",
        recipients=["email@address.com"],  # Replace with your email for test
        body="This is a test email from the integration test suite.",
        subtype=MessageType.plain,
    )

    mailer = get_email_client()
    await mailer.send_message(message)
