"""
Validation utilities for user input fields.

These functions raise `ValueError` with specific error codes when input fails
basic formatting or complexity requirements. Used with Pydantic validators
to enforce strong client-side and API-level validation.
"""

import string

import email_validator


def validate_email(email: str) -> None:
    """
    Validates that the given email has correct syntax.

    Args:
        email (str): The email string to validate.

    Raises:
        ValueError: If the email format is invalid.
    """
    try:
        # Skip deliverability checks for speed and privacy; only format is enforced
        email_validator.validate_email(email, check_deliverability=False)
    except email_validator.EmailNotValidError:
        raise ValueError("INVALID_EMAIL")


def validate_password(password: str) -> None:
    """
    Validates password length and complexity.

    Enforces:
    - Minimum length of 8
    - Maximum length of 128
    - Must include uppercase, lowercase, digit, and special character

    Args:
        password (str): The plaintext password to validate.

    Raises:
        ValueError: If the password is too short, too long, or lacks required characters.
    """
    if not password:
        raise ValueError("INVALID_PASSWORD")
    if len(password) < 8:
        raise ValueError("INVALID_PASSWORD")
    if len(password) > 128:
        raise ValueError("INVALID_PASSWORD")

    # Check for character class diversity
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    if not (has_lower and has_upper and has_digit and has_special):
        raise ValueError("INVALID_PASSWORD")
