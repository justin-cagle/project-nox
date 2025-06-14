import pytest


@pytest.mark.asyncio
async def test_api_auth_register(client):
    # Define a valid registration payload
    payload = {
        "email": "testuser@example.com",
        "password": "StrongPass123!",
        "user_name": "testuser",
        "display_name": "Test User",
    }

    # Send POST request to registration endpoint
    response = await client.post("/api/v1/auth/register", json=payload)

    # Assert HTTP status code
    assert response.status_code == 200

    # Parse response JSON
    data = response.json()

    # Assert expected response fields
    assert data["message"] == "Registration successful. Verification email sent."
    assert "userId" in data
    assert data["emailVerificationRequired"] is True
