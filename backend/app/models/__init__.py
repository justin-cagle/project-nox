# app/models/__init__.py

from .used_token import UsedToken
from .user import User

__all__ = [
    "User",
    "UsedToken",
]
