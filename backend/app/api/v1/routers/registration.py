from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.messages import Errors
from app.core.db import get_db
from app.core.limiting import limiter
from app.schemas.user import UserCreate
from app.services.onboarding import onboard_user

router = APIRouter()


@router.post("/register")
@limiter.limit("3/minute")
async def register_user(
    request: Request, user_in: UserCreate, db: AsyncSession = Depends(get_db)
):
    try:
        result = await onboard_user(user_in=user_in, db=db)
    except HTTPException as e:
        raise e

    if not result.get("success"):
        raise HTTPException(
            status_code=409, detail=result.get("detail", "Registration failed")
        )

    return {
        "message": "Registration successful. Verification email sent.",
        "userId": result["user_id"],
        "emailVerificationRequired": True,
    }
