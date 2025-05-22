from app.api.v1 import base
from app.core.config import settings
from fastapi import FastAPI

app = FastAPI(title=settings.app_name)

app.include_router(base.router, prefix="/api/v1")
