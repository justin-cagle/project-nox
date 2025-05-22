from app.core.db import SessionLocal
from app.schemas.user import UserCreate
from app.services.user import create_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/users")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await create_user(user_in, db)
        return {"id": user.id, "username": user.username, "email": user.email}
    except Exception:
        raise HTTPException(status_code=400, detail="User creation failed.")
