from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.limiting import limiter

router = APIRouter()


@router.get("/health")
@limiter.limit("5/minute")
async def get_heartbeat(request: Request):
    return JSONResponse(status_code=200, content={"message": "OK"})
