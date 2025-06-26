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
    mock_create_user.return_value = type("FakeUser", (), {"id": 123})()

    response = client.post(
        "/api/v1/auth/register", json=valid_request
    )  # should not raise
    assert response.status_code == 200
    resp_body = response.json()
    assert resp_body["message"] == "Registration successful. Verification email sent."
    assert resp_body["userId"] == 123
    assert resp_body["emailVerificationRequired"] is True

    mock_create_user.assert_called_once()


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "userexample.com",
        "user@.com",
        "user@com",
        "user@com.",
        "user@com..com",
        "a" * 255 + "@example.com",  # too long
    ],
)
def test_invalid_email(invalid_email):
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
        "PASSWORD123!",  # no lowercase (if you test with something like "PASSWORD123!")
        "password123!",  # no uppercase (if you test with "password123!")
        "A" * 129,  # too long
        "PasswordNoSpecial9",  # missing special
        "PASSWORD123!",  # missing lowercase
        "password123!",  # missing uppercase
    ],
)
def test_invalid_password(invalid_password):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "neo@example.com",
            "password": invalid_password,
            "user_name": "user.me",
            "display_name": "John Smith",
        },
    )
    assert response.status_code == 400
    resp_body = response.json()
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
    response = client.post("/api/v1/auth/register", json=missing_field)
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert "try again" in resp_body["errorMessage"].lower()


def test_empty_body():
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
    response = client.post("/api/v1/auth/register", json=invalid_type)
    resp_body = response.json()
    assert response.status_code == 400
    assert resp_body["error"]
    assert "errorCode" in resp_body
    assert "errorMessage" in resp_body
    assert "try again" in resp_body["errorMessage"].lower()


def test_non_json_body():
    response = client.post(
        "/api/v1/auth/register", data="not json", headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 400  # Unsupported Media Type
