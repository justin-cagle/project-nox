from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app.api.v1 import base
from app.core.config import settings
from app.exceptions.handlers import http_exception_handler, validation_exception_handler

app = FastAPI(title=settings.APP_NAME, debug=True)
app.add_exception_handler(
    RequestValidationError, validation_exception_handler
)  # type: ignore[arg-type]
app.add_exception_handler(
    HTTPException, http_exception_handler
)  # type: ignore[arg-type]

app.include_router(base.router, prefix="/api/v1")
