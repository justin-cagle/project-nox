import string

import email_validator


def validate_email(email: str) -> None:
    try:
        email_validator.validate_email(email, check_deliverability=False)
    except email_validator.EmailNotValidError:
        raise ValueError("INVALID_EMAIL")


def validate_password(password: str) -> None:
    if not password:
        raise ValueError("INVALID_PASSWORD")
    if len(password) < 8:
        raise ValueError("INVALID_PASSWORD")
    if len(password) > 128:
        raise ValueError("INVALID_PASSWORD")
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    if not (has_lower and has_upper and has_digit and has_special):
        raise ValueError("INVALID_PASSWORD")
