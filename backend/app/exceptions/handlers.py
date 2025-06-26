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
    response_data = {
        "error": "REGISTRATION_FAILED",
        "errorCode": "UNKNOWN_ERROR",
        "errorMessage": "Registration could not be completed. "
        "Please check your input and try again.",
    }

    if exc.status_code == 409:
        response_data["errorCode"] = "DUPLICATE_USER"

    return JSONResponse(status_code=exc.status_code, content=response_data)


def extract_error_info(exc: RequestValidationError) -> dict:
    for err in exc.errors():
        return {
            "errorCode": err.get("msg", "VALIDATION_ERROR"),
            "field": err.get("loc", ["unknown"])[-1],
        }
    return {"errorCode": "VALIDATION_ERROR", "field": None}
