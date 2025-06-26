from pydantic import BaseModel, field_validator

from app.validators.auth_validators import validate_email, validate_password


class UserCreate(BaseModel):
    email: str
    password: str
    user_name: str
    display_name: str

    @field_validator("email")
    def validate_email_field(cls, v):
        validate_email(v)
        return v

    @field_validator("password")
    def validate_password_field(cls, v):
        validate_password(v)
        return v
