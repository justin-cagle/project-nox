import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from app.core.base import Base


class UsedToken(Base):
    __tablename__ = "used_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_hash = Column(String, nullable=False, index=True)
    purpose = Column(String)
    created_at = Column(DateTime, default=func.now())
    redeemed_at = Column(DateTime, nullable=True)
    status = Column(String)
