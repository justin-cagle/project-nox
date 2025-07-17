"""
FastAPI application entry point.

This module initializes the FastAPI app instance, configures global exception
handlers, and registers the v1 API routes.
"""

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1 import base
from app.core.config import settings
from app.exceptions.handlers import http_exception_handler, validation_exception_handler

# Initialize the FastAPI app with a title from settings.
# `debug=True` enables detailed error pages during development.
# Make sure this is disabled in production.
app = FastAPI(title=settings.APP_NAME, debug=True)

# 👇 Use in-memory for now
limiter = Limiter(key_func=get_remote_address)

# Create your FastAPI app
app = FastAPI(...)

# Register middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register custom exception handler for request validation errors.
# type: ignore[arg-type] is used to silence type checker warnings related to handler signatures.
app.add_exception_handler(
    RequestValidationError, validation_exception_handler
)  # type: ignore[arg-type]

# Register custom exception handler for HTTP errors.
app.add_exception_handler(
    HTTPException, http_exception_handler
)  # type: ignore[arg-type]

# Include API version 1 routes with a common prefix.
app.include_router(base.router, prefix="/api/v1")
