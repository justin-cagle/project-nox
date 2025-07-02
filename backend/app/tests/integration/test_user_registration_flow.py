import uuid

import pytest


def unique_email():
    return f"{uuid.uuid4().hex[:8]}@example.com"


def unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio
async def test_api_auth_register(client):
    payload = {
        "email": unique_email(),
        "password": "ValidPassword1!",
        "user_name": unique_username(),
        "display_name": "Test User",
    }

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_missing_all_fields(client):
    response = await client.post("/api/v1/auth/register", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["field"] in {"email", "password", "user_name", "display_name"}


@pytest.mark.asyncio
async def test_register_missing_email(client):
    payload = {
        "password": "StrongPass123!",
        "user_name": unique_username(),
        "display_name": "Test user",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["field"] == "email"
    assert data["errorCode"].lower() == "field required"


@pytest.mark.asyncio
async def test_register_missing_password(client):
    payload = {
        "email": unique_email(),
        "user_name": unique_username(),
        "display_name": "Test user",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["field"] == "password"
    assert data["errorCode"].lower() == "field required"


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    payload = {
        "email": "not-an-email",
        "password": "StrongPass123!",
        "user_name": unique_username(),
        "display_name": "Test user",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["errorCode"] == "INVALID_EMAIL"


@pytest.mark.asyncio
async def test_register_duplicate_user(client):
    unique_id = str(uuid.uuid4())[:8]
    email = f"dupe_{unique_id}@example.com"
    username = f"dupeuser_{unique_id}"

    payload = {
        "email": email,
        "password": "ValidPassword1!",
        "user_name": username,
        "display_name": "Dupe User",
    }

    # First registration should succeed
    response1 = await client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == 200

    # Second registration should fail (duplicate)
    response2 = await client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409

    resp_body = response2.json()
    assert resp_body["error"] == "REGISTRATION_FAILED"
    assert resp_body["errorCode"] == "DUPLICATE_USER"
    assert "already exists" in resp_body["errorMessage"].lower()
