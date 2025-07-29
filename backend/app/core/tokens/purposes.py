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
        SESSION: Short-duration token for session identity. (15 minute duration)
        REFRESH: Long-duration token used for login expiration and reissuance. (7 day duration)
    """

    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    SESSION = "auth_session"
    REFRESH = "auth_refresh"
    # Add more as needed above this comment
