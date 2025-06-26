import pytest


@pytest.mark.asyncio
async def test_api_auth_register(client):
    payload = {
        "email": "testuser@example.com",
        "password": "StrongPass123!",
        "user_name": "testuser",
        "display_name": "Test user",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Registration successful. Verification email sent."
    assert "userId" in data
    assert data["emailVerificationRequired"] is True


@pytest.mark.asyncio
async def test_register_missing_all_fields(client):
    payload = {}
    response = await client.post("/api/v1/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["field"] in {"email", "password", "user_name", "display_name"}


@pytest.mark.asyncio
async def test_register_missing_email(client):
    payload = {
        "password": "StrongPass123!",
        "user_name": "testuser",
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
        "email": "testuser@example.com",
        "user_name": "testuser",
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
        "user_name": "testuser",
        "display_name": "Test user",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["errorCode"] == "INVALID_EMAIL"


@pytest.mark.asyncio
async def test_register_duplicate_user(client):
    payload = {
        "email": "dupe@example.com",
        "password": "ValidPassword1!",
        "user_name": "dupeuser",
        "display_name": "Dupe User",
    }

    # First registration should succeed
    response1 = await client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == 200

    # Second registration should fail
    response2 = await client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409

    resp_body = response2.json()
    assert resp_body["error"] == "REGISTRATION_FAILED"
    assert resp_body["errorCode"] == "DUPLICATE_USER"
    assert "try again" in resp_body["errorMessage"].lower()
