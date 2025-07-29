from app.schemas.auth import LoginRequest


def test_login_request_alias_parsing():
    data = {
        "identifier": "user@example.com",
        "password": "SecurePass1!",
        "rememberMe": True,
    }

    model = LoginRequest(**data)
    assert model.remember_me is True
