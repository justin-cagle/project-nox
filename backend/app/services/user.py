from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(user_in: UserCreate, db: AsyncSession) -> User:
    user = User(username=user_in.username, email=user_in.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
