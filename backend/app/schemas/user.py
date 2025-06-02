from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    user_name: str
    display_name: str
