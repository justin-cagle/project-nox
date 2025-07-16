"""
Custom exception handlers and error utilities for FastAPI.

This module provides handlers for:
- Pydantic validation errors
- Generic HTTP exceptions
- ValueErrors raised internally
It also includes token validation error classes and input error parsing logic.

All responses are sanitized to avoid leaking internal details, and structured
for consistent frontend consumption.
"""

from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handles validation errors from FastAPI/Pydantic input models.

    Args:
        request (Request): The incoming request object.
        exc (RequestValidationError): The raised validation error.

    Returns:
        JSONResponse: A generic but structured error response with field context.
    """
    error_info = extract_error_info(exc)

    return JSONResponse(
        status_code=400,
        content={
            "error": "REGISTRATION_FAILED",
            "errorCode": error_info["errorCode"],
            "field": error_info["field"],
            "errorMessage": "Registration could not be completed. "
            "Please check your input and try again.",
        },
    )


async def value_error_exception_handler(
    request: Request, exc: ValueError
) -> JSONResponse:
    """
    Converts raw Python ValueErrors into HTTP 400 responses.

    Args:
        request (Request): The incoming request.
        exc (ValueError): The raised error.

    Returns:
        JSONResponse: A generic 400 with error detail.
    """
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles FastAPI-raised HTTPExceptions, customizing format when possible.

    Args:
        request (Request): The incoming request.
        exc (HTTPException): The raised exception.

    Returns:
        JSONResponse: A structured response with optional custom codes.
    """
    # If a dict was passed as the .detail, trust it and return directly
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    # Otherwise, fallback to generic safe message
    response_data = {
        "error": "REGISTRATION_FAILED",
        "errorCode": "UNKNOWN_ERROR",
        "errorMessage": str(exc.detail) if exc.detail else "Something went wrong.",
    }

    # If status code is 409, likely duplicate user
    if exc.status_code == 409:
        response_data["errorCode"] = "DUPLICATE_USER"

    return JSONResponse(status_code=exc.status_code, content=response_data)


def extract_error_info(exc: RequestValidationError) -> dict:
    """
    Parses FastAPI validation error object to extract a structured field + code.

    Args:
        exc (RequestValidationError): The validation exception raised.

    Returns:
        dict: A dictionary with keys `errorCode` and `field`.
    """
    for err in exc.errors():
        msg = err.get("msg", "VALIDATION_ERROR")
        # Allow "message,CODE" format in Pydantic error messages for custom errorCode support
        if "," in msg:
            _, code = msg.split(",", 1)
            error_code = code.strip()
        else:
            error_code = msg
        return {
            "errorCode": error_code,
            "field": err.get("loc", ["unknown"])[-1],
        }

    # Fallback if no errors found
    return {"errorCode": "VALIDATION_ERROR", "field": None}


class TokenValidationError(Exception):
    """
    Raised when a token is invalid, expired, reused, or fails validation.

    This custom exception integrates with your JWT and token validation flow
    and can be caught for structured 400 responses.
    """

    def __init__(self, detail: str = "Invalid or expired token"):
        self.detail = detail

    def __str__(self):
        return self.detail
