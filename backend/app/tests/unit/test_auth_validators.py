import pytest

from app.validators import auth_validators

# --- Email Validation Tests ---


@pytest.mark.parametrize(
    "valid_email",
    [
        "user@example.com",
        "user.name+test@example.co.uk",
        "user_name@example.io",
        "user-name@subdomain.example.com",
    ],
)
def test_valid_email(valid_email):
    auth_validators.validate_email(valid_email)  # should not raise


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
    with pytest.raises(ValueError) as exc_info:
        auth_validators.validate_email(invalid_email)
    assert "email" in str(exc_info.value).lower()


# --- Password Validation Tests ---


@pytest.mark.parametrize(
    "valid_password",
    ["StrongPass1!", "Another$Pass123", "Xyz@123abc", "Valid$Password9"],
)
def test_valid_password(valid_password):
    auth_validators.validate_password(valid_password)  # should not raise


@pytest.mark.parametrize(
    "invalid_password",
    [
        "",  # empty
        "short",  # too short
        "alllowercase",  # no upper, no digit, no special
        "ALLUPPERCASE",  # no lower, no digit, no special
        "NoSpecial123",  # no special
        "NoNumber!",  # no number
        "PASSWORD123!",  # no lowercase (if something like "PASSWORD123!")
        "password123!",  # no uppercase (if you test with "password123!")
        "A" * 129,  # too long
        "PasswordNoSpecial9",  # missing special
        "PASSWORD123!",  # missing lowercase
        "password123!",  # missing uppercase
    ],
)
def test_invalid_password(invalid_password):
    with pytest.raises(ValueError) as exc_info:
        auth_validators.validate_password(invalid_password)
    assert "password" in str(exc_info.value).lower()
