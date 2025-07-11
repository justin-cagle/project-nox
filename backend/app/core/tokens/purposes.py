from enum import Enum


class TokenPurpose(str, Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    # Add more as needed above this comment
