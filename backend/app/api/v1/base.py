from fastapi import APIRouter

from app.api.v1.routers import health, login, registration, verify

api_router = APIRouter()

api_router.include_router(registration.router, prefix="/auth", tags=["Auth"])
api_router.include_router(verify.router, prefix="/auth", tags=["Auth"])
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(login.router, prefix="/auth", tags=["Auth"])
