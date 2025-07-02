from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
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
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
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
    for err in exc.errors():
        msg = err.get("msg", "VALIDATION_ERROR")
        if "," in msg:
            _, code = msg.split(",", 1)
            error_code = code.strip()
        else:
            error_code = msg
        return {
            "errorCode": error_code,
            "field": err.get("loc", ["unknown"])[-1],
        }
    return {"errorCode": "VALIDATION_ERROR", "field": None}
