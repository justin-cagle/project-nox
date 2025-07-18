from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.core.logging import setup_logger_from_settings

# In the future: from app.services.telemetry import shutdown_telemetry


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup logic
    setup_logger_from_settings()
    logger.info("Project Nox starting up")

    # 👇 You can add telemetry init here later

    yield  # --- app runs here ---

    # ✅ Shutdown logic
    logger.info("Project Nox shutting down")

    # 👇 Add telemetry flush/cleanup later
