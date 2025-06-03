from app.core.db import SessionLocal
from app.schemas.user import UserCreate
from app.services.user import create_user
from app.validators import auth_validators
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/auth/register")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        auth_validators.validate_email(user_in.email)
        auth_validators.validate_password(user_in.password)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "REGISTRATION_FAILED",
                "errorCode": str(e),
                "errorMessage": "Registration could "
                "not be completed. "
                "Please check your input and try again.",
            },
        )
    user = await create_user(user_in, db)

    return {
        "message": "Registration successful. Verification email sent.",
        "userId": user.id,
        "emailVerificationRequired": True,
    }
