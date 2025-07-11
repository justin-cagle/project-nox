from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class UsedToken(BaseModel):
    id: UUID
    user_id: UUID
    token_hash: str
    issued_at: datetime
    created_at: datetime


class VerifyEmailToken(BaseModel):
    token: str
