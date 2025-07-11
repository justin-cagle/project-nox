"""
Comprehensive unit tests for the `/auth/register` endpoint.

Covers:
- Happy path (valid input, mocked user creation)
- Field-level validation for:
    - Email format
    - Password strength
    - Missing required fields
    - Incorrect field types
- Empty and non-JSON payloads
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "valid_request",
    [
        {
            "email": "neo@example.com",
            "password": "ValidPassword1!",
            "user_name": "user.me",
            "display_name": "John Smith",
        }
    ],
)
@patch("app.api.v1.base.create_user", new_callable=AsyncMock)
def test_create_valid_user(mock_create_user, valid_request):
    """
    Test a valid registration flow with mocked user creation.

    Asserts:
        - HTTP 200 OK
        - Email verification required
        - Correct user ID returned
        - Backend function is called exactly once
    """
    mock_create_user.return_value = type("FakeUser", (), {"id": 123})()

    response = client.post("/api/v1/auth/register", json=valid_request)
    assert response.status_code == 200
    resp_body = response.json()
    assert resp_body["message"] == "Registration successful. Verification email sent."
    assert resp_body["userId"] == 123
    assert resp_body["emailVerificationRequired"] is True

    mock_create_user.assert_called_once()


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",  # empty
        "userexample.com",  # missing @
        "user@.com",  # domain starts with dot
        "user@com",  # no TLD
        "user@com.",  # trailing dot
        "user@com..com",  # double dot
        "a" * 255 + "@example.com",  # too long
    ],
)
def test_invalid_email(invalid_email):
    """
    Submit invalid emails and verify validation failure.

    Asserts:
        - 400 response
        - Email-specific error field and code
    """
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": invalid_email,
            "password": "ValidPassword!",
            "user_name": "user.me",
            "display_name": "John Smith",
        },
    )
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert resp_body["field"] == "email"
    assert "try again" in resp_body["errorMessage"].lower()


@pytest.mark.parametrize(
    "invalid_password",
    [
        "",  # empty
        "short",  # too short
        "alllowercase",  # no upper, no digit, no special
        "ALLUPPERCASE",  # no lower, no digit, no special
        "NoSpecial123",  # no special
        "NoNumber!",  # no number
        "PASSWORD123!",  # no lowercase
        "password123!",  # no uppercase
        "A" * 129,  # too long
        "PasswordNoSpecial9",
        "PASSWORD123!",
        "password123!",
    ],
)
def test_invalid_password(invalid_password):
    """
    Validate rejection of weak or invalid passwords.

    Asserts:
        - 400 error
        - Password-specific error field
    """
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "neo@example.com",
            "password": invalid_password,
            "user_name": "user.me",
            "display_name": "John Smith",
        },
    )
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert resp_body["field"] == "password"
    assert "try again" in resp_body["errorMessage"].lower()


@pytest.mark.parametrize(
    "missing_field",
    [
        {
            # Missing email
            "password": "ValidPassword!",
            "user_name": "user.me",
            "display_name": "John Smith",
        },
        {
            # Missing password
            "email": "neo@example.com",
            "user_name": "user.me",
            "display_name": "John Smith",
        },
        {
            # Missing user name
            "email": "neo@example.com",
            "password": "ValidPassword!",
            "display_name": "John Smith",
        },
        {
            # Missing display name
            "email": "neo@example.com",
            "password": "ValidPassword!",
            "user_name": "user.me",
        },
    ],
)
def test_missing_field(missing_field):
    """
    Omit required fields one at a time and verify error responses.

    Asserts:
        - 400 error
        - Generic safe error response with helpful message
    """
    response = client.post("/api/v1/auth/register", json=missing_field)
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert "try again" in resp_body["errorMessage"].lower()


def test_empty_body():
    """
    Submit an empty JSON object and expect full validation failure.
    """
    response = client.post("/api/v1/auth/register", json={})
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert "try again" in resp_body["errorMessage"].lower()


@pytest.mark.parametrize(
    "invalid_type",
    [
        {
            "email": 1234,
            "password": "ValidPassword!",
            "user_name": "user.me",
            "display_name": "John Smith",
        },
        {
            "email": "neo@example.com",
            "password": 1234,
            "user_name": "user.me",
            "display_name": "John Smith",
        },
        {
            "email": "neo@example.com",
            "password": "ValidPassword!",
            "user_name": 1234,
            "display_name": "John Smith",
        },
        {
            "email": "neo@example.com",
            "password": "ValidPassword!",
            "user_name": "user.me",
            "display_name": 1234,
        },
    ],
)
def test_invalid_field_type(invalid_type):
    """
    Provide fields with incorrect types (e.g., int instead of str).

    Asserts:
        - 400 validation error
        - Appropriate error message returned
    """
    response = client.post("/api/v1/auth/register", json=invalid_type)
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert "try again" in resp_body["errorMessage"].lower()


def test_non_json_body():
    """
    Submit non-JSON content with wrong content type header.

    Asserts:
        - 400 error due to invalid media type
    """
    response = client.post(
        "/api/v1/auth/register",
        content="not json",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 400
