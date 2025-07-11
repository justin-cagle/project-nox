from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.db import get_db
from app.core.tokens.purposes import TokenPurpose
from app.exceptions.handlers import TokenValidationError
from app.schemas.auth import VerifyEmailToken
from app.schemas.user import UserCreate
from app.services.user import create_user
from app.core.tokens.base import validate_token

router = APIRouter()


@router.post("/auth/register")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(user_in, db)
    return {
        "message": "Registration successful. Verification email sent.",
        "userId": user.id,
        "emailVerificationRequired": True,
    }


@router.get("/auth/verify")
async def verify_email(query: VerifyEmailToken = Depends(),
                       db: AsyncSession = Depends(get_db)
                       ):
    try:
        user_id = await validate_token(token=query.token,
                                       purpose=TokenPurpose.EMAIL_VERIFICATION,
                                       secret=settings.EMAIL_TOKEN_SECRET,
                                       db=db
                                       )
    except TokenValidationError as e:
        return JSONResponse(
            status_code=400,
            content={
                        "status": "error",
                        "error_code": "invalid_token",
                        "message": str(e),
                    }
        )

    return {
        "status": "success",
        "message": "Email verification token is valid."
    }


@router.get("/db-check")
async def db_check(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"db_ok": result.scalar() == 1}
