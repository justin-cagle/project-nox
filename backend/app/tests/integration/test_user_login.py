import pytest
from pydantic_core.core_schema import JsonSchema

from app.models import User
from app.tests.integration.conftest import unique_email, unique_username


@pytest.mark.asyncio
async def test_user_valid_login(client):
    user = await create_test_user(client)

    # Attempt to login as inserted user
    credentials = {
        "identifier": user["email"],
        "password": user["password"],
        "remember_me": True,
    }

    login_response = await client.post("/api/v1/routers/auth/login", json=credentials)
    data = login_response.json()

    assert isinstance(data["sessionToken"], str)
    assert isinstance(data["refreshToken"], str)
    assert data["expiresIn"] > 0
    assert data["refreshTokenExpiresIn"] > 0


@pytest.mark.parametrize("credentials", ["wrong_id", "wrong_pass"])
@pytest.mark.asyncio
async def test_user_invalid_credentials(client, credentials):
    user = await create_test_user(client)

    # Attempt to login as inserted user
    base_credentials = {
        "identifier": user["email"],
        "password": user["password"],
        "remember_me": True,
    }

    match credentials:
        case "wrong_id":
            base_credentials["identifier"] = "not_a_user"
        case "wrong_pass":
            base_credentials["password"] = "blah"
        case _:
            pass

    login_response = await client.post(
        "/api/v1/routers/auth/login", json=base_credentials
    )
    assert login_response.status_code in [401, 403]


async def create_test_user(client) -> dict:
    payload = {
        "email": unique_email(),
        "password": "ValidPassword1!",
        "user_name": unique_username(),
        "display_name": "Test User",
    }

    # Insert user in the DB
    response = await client.post("/api/v1/routers/auth/register", json=payload)
    assert response.status_code == 200

    return payload
