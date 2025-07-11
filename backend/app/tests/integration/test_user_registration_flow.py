"""
Integration tests for the user registration flow.

These tests verify:
- Successful user registration with valid input
- Error responses for missing or incomplete payloads
- Server-side validation feedback consistency
"""

import uuid

import pytest


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
async def test_api_auth_register(client):
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

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["emailVerificationRequired"] is True
    assert data["userId"]


@pytest.mark.asyncio
async def test_register_missing_all_fields(client):
    """
    Submit empty payload and assert field-level validation.

    Asserts:
        - HTTP 400 error
        - One of the required fields is reported
    """
    response = await client.post("/api/v1/auth/register", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["field"] in {"email", "password", "user_name", "display_name"}


@pytest.mark.asyncio
async def test_register_missing_email(client):
    """
    Submit registration with missing email and assert correct error.

    Asserts:
        - HTTP 400 error
        - Field context in response
    """
    payload = {
        "password": "StrongPass123!",
        "user_name": unique_username(),
        "display_name": "Test user",
    }

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["field"] == "email"
