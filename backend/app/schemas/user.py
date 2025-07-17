"""
Pydantic schemas related to user creation and registration.

These schemas define the shape of user input and include field-level validators
to enforce proper email and password formatting during registration.
"""

import re

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
    @classmethod
    def validate_email_field(cls, v):
        validate_email(v)
        return v

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v):
        validate_password(v)
        return v

    @field_validator("user_name")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("USERNAME_BLANK")
        return v

    @field_validator("user_name")
    @classmethod
    def only_safe_chars(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_.]+$", v):
            raise ValueError("USERNAME_INVALID")
        return v

    @field_validator("user_name", mode="before")
    @classmethod
    def strip_input(cls, v) -> str:
        if not isinstance(v, str):
            raise ValueError("USERNAME_NOT_STRING")
        return v.strip()
