from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.user import UserCreate
from app.services.user import create_user

router = APIRouter()


@router.post("/auth/register")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await create_user(user_in, db)
    return {
        "message": "Registration successful. Verification email sent.",
        "userId": user.id,
        "emailVerificationRequired": True,
    }
