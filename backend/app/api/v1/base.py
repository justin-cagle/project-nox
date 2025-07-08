from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.user import UserCreate
from app.services.user import create_user

router = APIRouter()


@router.post("/auth/register")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(user_in, db)
    return {
        "message": "Registration successful. Verification email sent.",
        "userId": user.id,
        "emailVerificationRequired": True,
    }

@router.get("/db-check")
async def db_check(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"db_ok": result.scalar() == 1}
