"""
Enumerates supported token use-cases for the token service.

Used to assign, verify, and track token intent (e.g. email verification, password reset).
"""

from enum import Enum


class TokenPurpose(str, Enum):
    """
    Enum representing valid purposes for one-time tokens.

    Values:
        EMAIL_VERIFICATION: Token issued to confirm email ownership.
        PASSWORD_RESET: Token issued to authorize a password reset.
    """

    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    # Add more as needed above this comment
