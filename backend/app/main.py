"""
FastAPI application entry point.

This module initializes the FastAPI app instance, configures global exception
handlers, and registers the v1 API routes.
"""

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.api.v1 import base
from app.core.config import settings
from app.core.lifespan import lifespan  # ✅ NEW: lifespan support
from app.core.limiting import limiter
from app.exceptions.handlers import (
    http_exception_handler,
    rate_limit_handler,
    validation_exception_handler,
)

# Initialize the FastAPI app with a title from settings and lifespan hook.
app = FastAPI(
    title=settings.APP_NAME,
    debug=True,  # ⚠️ Make sure to override via settings in prod
    lifespan=lifespan,  # ✅ Hook in the lifespan context manager
)

# Register middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# Register custom exception handlers
app.add_exception_handler(
    RequestValidationError, validation_exception_handler
)  # type: ignore[arg-type]

app.add_exception_handler(
    HTTPException, http_exception_handler
)  # type: ignore[arg-type]

# Include API version 1 routes with a common prefix.
app.include_router(base.api_router, prefix="/api/v1/routers")
