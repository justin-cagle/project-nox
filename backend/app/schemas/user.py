"""
Pydantic schemas related to user creation and registration.

These schemas define the shape of user input and include field-level validators
to enforce proper email and password formatting during registration.
"""

from pydantic import BaseModel, field_validator

from app.validators.auth_validators import validate_email, validate_password


class UserCreate(BaseModel):
    """
    Schema for user registration input.

    Attributes:
        email (str): The user's email address.
        password (str): Plaintext password to be validated and hashed.
        user_name (str): Unique username for the user.
        display_name (str): Friendly display name for the user.
    """

    email: str
    password: str
    user_name: str
    display_name: str

    @field_validator("email")
    def validate_email_field(cls, v):
        """
        Validates that the email is in a proper format using a shared validator.
        """
        validate_email(v)
        return v

    @field_validator("password")
    def validate_password_field(cls, v):
        """
        Validates that the password meets complexity and formatting rules.
        """
        validate_password(v)
        return v
