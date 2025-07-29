from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.constants.messages import Auth
from app.core.db import get_db
from app.core.security import check_password, hash_password
from app.schemas.auth import LoginRequest
from app.services.user import get_user_by_email, get_user_by_username

router = APIRouter()


@router.post("/login")
async def login_user(
    request: Request, credentials: LoginRequest, db: AsyncSession = Depends(get_db)
):
    identifier = credentials.identifier.strip().lower()

    try:
        if "@" in identifier:
            user = await get_user_by_email(identifier, db)
        else:
            user = await get_user_by_username(identifier, db)
    except HTTPException:
        raise HTTPException(status_code=401, detail=Auth.INVALID_CREDENTIALS)

    if user.is_locked:
        raise HTTPException(status_code=403, detail=Auth.LOCKED)

    if not check_password(
        password=credentials.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401, detail=Auth.INVALID_CREDENTIALS)

    return JSONResponse(status_code=200, content={"message": Auth.LOGIN_SUCCESS})
