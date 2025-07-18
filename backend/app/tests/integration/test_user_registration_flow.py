"""
Integration tests for the user registration flow.

These tests verify:
- Successful user registration with valid input
- Error responses for missing or incomplete payloads
- Server-side validation feedback consistency
"""

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.constants.messages import Registration
from app.core.tokens.purposes import TokenPurpose
from app.core.tokens.status import TokenStatus
from app.models import UsedToken, User


def unique_email():
    """
    Generates a unique dummy email address for testing.
    """
    return f"{uuid.uuid4().hex[:8]}@example.com"


def unique_username():
    """
    Generates a unique dummy username for testing.
    """
    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio
async def test_api_auth_register(client, db_session):
    """
    Test full registration flow with valid user input.

    Asserts:
        - HTTP 200 response
        - Email verification trigger
        - User ID returned
    """
    payload = {
        "email": unique_email(),
        "password": "ValidPassword1!",
        "user_name": unique_username(),
        "display_name": "Test User",
    }

    # Insert user in the DB
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["emailVerificationRequired"] is True
    assert data["userId"]

    # Ensure that the user can be retrieved
    stmt = select(User).where(User.email == payload["email"])
    result = await db_session.execute(stmt)
    user = result.scalar_one()

    # Validate that it's the same user and inserted correctly
    assert user.username == payload["user_name"]
    assert user.email == payload["email"]
    assert user.hashed_password != payload["password"]
    assert user.display_name == payload["display_name"]
    assert user.is_verified is False

    # Retrieve the issued token from the DB
    stmt = select(UsedToken).where(UsedToken.user_id == user.id)
    result = await db_session.execute(stmt)
    token = result.scalar_one()

    # Validate the token is the same and inserted correctly
    assert token is not None
    assert token.token_hash is not None
    assert token.purpose == TokenPurpose.EMAIL_VERIFICATION
    assert token.created_at < datetime.now(tz=timezone.utc)
    assert token.redeemed_at is None
    assert token.status == TokenStatus.ISSUED


@pytest.mark.parametrize(
    "missing_field", ["email", "password", "user_name", "display_name"]
)
@pytest.mark.asyncio
async def test_register_missing_fields(client, missing_field):
    """
    Submit a payload missing one required field and assert correct validation error.

    Asserts:
        - HTTP 400 response
        - 'field' in response matches the omitted field
    """
    payload = {
        "email": unique_email(),
        "password": "ValidPassword1!",
        "user_name": unique_username(),
        "display_name": "Test User",
    }

    del payload[missing_field]

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["field"] == missing_field


@pytest.mark.parametrize("dupe", ["email", "user_name"])
@pytest.mark.asyncio
async def test_duplicate_registration(client, dupe, db_session):
    email = unique_email()
    user_name = unique_username()

    payload = {
        "email": email,
        "password": "ValidPassword1!",
        "user_name": user_name,
        "display_name": "Test User",
    }

    # First registration should succeed
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    print("FIRST RESPONSE JSON:", response.json())

    dupe_payload = {
        "email": email if dupe == "email" else unique_email(),
        "password": "ValidPassword1!",
        "user_name": user_name if dupe == "user_name" else unique_username(),
        "display_name": "Test User",
    }

    users = await db_session.execute(select(User))

    # Second registration should fail
    response = await client.post("/api/v1/auth/register", json=dupe_payload)
    data = response.json()
    assert response.status_code == 409
    assert data["errorCode"] == "DUPLICATE_USER"
    assert data["errorMessage"] == Registration.DUPE_USER


@pytest.mark.parametrize(
    "field,value,expected_field",
    [
        ("email", "not-an-email", "email"),
        ("email", "user@example.com ", "email"),
        ("user_name", "      ", "user_name"),
        ("user_name", "user<script>", "user_name"),
        ("display_name", "Z̴̰͑a̸͙̾l̸̼̃g̷͍̊o̶̱͌", None),  # may or may not be rejected
        ("password", "123", "password"),
    ],
)
@pytest.mark.asyncio
async def test_register_field_edge_cases(client, field, value, expected_field):
    payload = {
        "email": "user@example.com",
        "password": "ValidPassword1!",
        "user_name": "safe_user",
        "display_name": "Normal Name",
    }

    payload[field] = value
    response = await client.post("/api/v1/auth/register", json=payload)

    # If expected_field is None, we expect success
    if expected_field is None:
        assert response.status_code == 200
    else:
        assert response.status_code == 400
        data = response.json()
        assert data["field"] == expected_field


@pytest.mark.asyncio
async def test_register_rate_limit(client):
    payload = {
        "email": unique_email(),
        "password": "ValidPassword1!",
        "user_name": unique_username(),
        "display_name": "Test User",
    }

    # Make 3 successful requests
    for _ in range(3):
        response = await client.post("/api/v1/auth/register", json=payload)
        assert response.status_code in {200, 400}  # allow validation to block reuse

        # Change payload slightly to avoid validation rejection
        payload["email"] = unique_email()
        payload["user_name"] = unique_username()

    # 4th request should be blocked
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 429
    data = response.json()
    assert data["errorCode"] == "RATE_LIMITED"
