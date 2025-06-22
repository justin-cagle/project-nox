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
