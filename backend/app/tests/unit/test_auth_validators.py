"""
Unit tests for custom email validation logic.

These tests verify:
- Accepted email formats using a variety of syntaxes
- Rejection of malformed or invalid formats
- Edge case handling for RFC-like variants and common mistakes
"""

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
        "customer/department=shipping@example.com",
        "$A12345@example.com",
        "!def!xyz%abc@example.com",
    ],
)
def test_valid_email(valid_email):
    """
    Ensure that all valid email formats pass without raising.

    Args:
        valid_email (str): A known-valid email format.

    Asserts:
        No exception is raised.
    """
    auth_validators.validate_email(valid_email)  # should not raise


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",  # Empty string
        "plainaddress",  # No @
        "@no-local-part.com",  # Missing local part
        "Outlook Contact <outlook-contact@domain.com>",  # Name in address
        "no-at.domain.com",  # Missing @ symbol
        "no-tld@domain",  # Missing top-level domain
        "lots-of-dots@domain..com",  # Double dot
        "trailing-dot@domain.com.",  # Trailing dot
        ".leading-dot@domain.com",  # Leading dot in local part
        "spaces in@email.com",  # Space in address
        "user@.invalid.com",  # Domain starts with dot
        "user@[192.168.1.256]",  # Invalid IPv4 literal
        "user@localhost",  # Localhost often rejected in production
        "a" * 255 + "@example.com",  # Exceeds max length
    ],
)
def test_invalid_email(invalid_email):
    """
    Ensure that invalid emails raise ValueError.

    Args:
        invalid_email (str): A malformed or unacceptable email string.

    Asserts:
        ValueError is raised for each.
    """
    with pytest.raises(ValueError, match="INVALID_EMAIL"):
        auth_validators.validate_email(invalid_email)
