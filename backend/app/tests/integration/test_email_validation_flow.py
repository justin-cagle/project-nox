from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from conftest import unique_email, unique_username
from httpx import AsyncClient
from jose import jwt
from sqlalchemy import select

from app.constants.messages import Verification
from app.core.config import settings
from app.core.security import hash_str
from app.core.tokens.base import decode_token
from app.core.tokens.purposes import TokenPurpose
from app.core.tokens.status import TokenStatus
from app.models import UsedToken, User


@pytest.mark.asyncio
async def test_email_validation(client, db_session, disable_real_emails: AsyncMock):
    """Test that a valid email verification token passes validation and mutates user/token state.

    Args:
        client (AsyncClient): The HTTP client for testing routes.
        db_session (AsyncSession): The test database session.
        disable_real_emails (AsyncMock): The monkeypatched email-sending mock.
    """
    token, user_id = await register_test_user(
        client,
        email=unique_email(),
        username=unique_username(),
        disable_real_emails=disable_real_emails,
    )

    verification_url = f"/api/v1/auth/verify?token={token}"
    response = await client.get(verification_url)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == Verification.SUCCESS

    await assert_token_redeemed(token, db_session)
    await assert_user_verified(user_id, db_session)


@pytest.mark.parametrize(
    "attribute", ["time", "purpose", "secret", "algorithm", "missing", "malformed"]
)
@pytest.mark.asyncio
async def test_email_validation_altered_token(
    client, db_session, disable_real_emails: AsyncMock, attribute
):
    token, _ = await register_test_user(
        client=client,
        email=unique_email(),
        username=unique_username(),
        disable_real_emails=disable_real_emails,
    )

    bad_token = decode_and_modify_token_attribute(token, attribute)

    verification_url = f"/api/v1/auth/verify?token={bad_token}"
    response = await client.get(verification_url)

    assert response.status_code == 400
    data = response.json()
    assert data["message"] in [
        "Token could not be decoded",
        "Token not found or already used",
        "Token subject is invalid or missing",
    ]


async def register_test_user(
    client: AsyncClient,
    email: str,
    username: str,
    disable_real_emails: AsyncMock,
) -> tuple[str, UUID]:
    payload = {
        "email": email,
        "password": "ValidPassword1!",
        "user_name": username,
        "display_name": "Test User",
    }

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    user_id = UUID(response.json()["userId"])

    assert disable_real_emails.await_args is not None
    _, kwargs = disable_real_emails.await_args
    token = kwargs["token"]

    return token, user_id


@pytest.mark.asyncio
async def test_resend_verification_known_user(
    client: AsyncClient, db_session, disable_real_emails: AsyncMock
):
    email = unique_email()
    username = unique_username()

    # Register a test user
    payload = {
        "email": email,
        "password": "ValidPassword1!",
        "user_name": username,
        "display_name": "Test User",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200

    # Try to resend using email
    resend_email = await client.post(
        "/api/v1/auth/verify/resend", params={"email": email}
    )
    assert resend_email.status_code == 200
    assert "verification email was sent" in resend_email.json()["message"]

    # Try to resend using username
    resend_username = await client.post(
        "/api/v1/auth/verify/resend", params={"username": username}
    )
    assert resend_username.status_code == 200
    assert "verification email was sent" in resend_username.json()["message"]


@pytest.mark.asyncio
async def test_resend_verification_unknown_user(client: AsyncClient):
    # Try with non-existent email
    response = await client.post(
        "/api/v1/auth/verify/resend", params={"email": "ghost@example.com"}
    )
    assert response.status_code == 200
    assert "verification email was sent" in response.json()["message"]

    # Try with non-existent username
    response = await client.post(
        "/api/v1/auth/verify/resend", params={"username": "notarealuser"}
    )
    assert response.status_code == 200
    assert "verification email was sent" in response.json()["message"]


def decode_and_modify_token_attribute(token: str, attribute: str):
    decoded_token = decode_token(
        token=token,
        expected_purpose=TokenPurpose.EMAIL_VERIFICATION,
        secret=settings.EMAIL_TOKEN_SECRET,
    )

    if attribute == "time":
        expired = datetime.now(tz=timezone.utc) - timedelta(minutes=60)
        return jwt.encode(
            {
                "sub": decoded_token["sub"],
                "exp": expired,
                "purpose": decoded_token["purpose"],
            },
            settings.EMAIL_TOKEN_SECRET,
            algorithm="HS256",
        )
    elif attribute == "purpose":
        return jwt.encode(
            {
                "sub": decoded_token["sub"],
                "exp": decoded_token["exp"],
                "purpose": TokenPurpose.PASSWORD_RESET,
            },
            settings.EMAIL_TOKEN_SECRET,
            algorithm="HS256",
        )
    elif attribute == "secret":
        return jwt.encode(
            {
                "sub": decoded_token["sub"],
                "exp": decoded_token["exp"],
                "purpose": decoded_token["purpose"],
            },
            "wrong.secret",
            algorithm="HS256",
        )
    elif attribute == "algorithm":
        return jwt.encode(
            {
                "sub": decoded_token["sub"],
                "exp": decoded_token["exp"],
                "purpose": decoded_token["purpose"],
            },
            settings.EMAIL_TOKEN_SECRET,
            algorithm="HS512",
        )
    elif attribute == "missing":
        return jwt.encode(
            {"exp": decoded_token["exp"], "purpose": decoded_token["purpose"]},
            settings.EMAIL_TOKEN_SECRET,
            algorithm="HS256",
        )
    elif attribute == "malformed":
        return "not.a.token"

    return None


async def assert_token_redeemed(token: str, db_session):
    token_hash = hash_str(token, TokenPurpose.EMAIL_VERIFICATION)
    stmt = select(UsedToken).where(UsedToken.token_hash == token_hash)
    result = await db_session.execute(stmt)
    token_record = result.scalar_one()
    assert token_record.status == TokenStatus.REDEEMED
    assert token_record.redeemed_at is not None


async def assert_user_verified(user_id: UUID, db_session):
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user = result.scalar_one()
    assert user.is_verified is True
