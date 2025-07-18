import logging
import os
import sys
from pathlib import Path

from loguru import logger


def setup_logger(
    log_file: str | None = None, *, debug: bool = False, json_output: bool = False
):
    """
    Initializes the global loguru logger.

    Args:
        log_file: Optional path to log file (rotated & retained).
        debug: Enable DEBUG level logging.
        json_output: Output logs as structured JSON (for prod/telemetry ingestion).
    """
    # Clear default handler
    logger.remove()

    log_level = "DEBUG" if debug else "INFO"

    if os.getenv("PYTEST_CURRENT_TEST") is not None:

        class InterceptHandler(logging.Handler):
            def emit(self, record):
                # Propagate loguru messages to standard logging
                logging.getLogger(record.name).handle(record)

        logger.add(InterceptHandler(), level=log_level)

    # Pretty console logging for dev
    logger.add(
        sys.stdout,
        level=log_level,
        serialize=json_output,
        format=(
            (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            )
            if not json_output
            else None
        ),
        backtrace=True,
        diagnose=debug,
    )

    # Optional file logging with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            str(log_path),
            level=log_level,
            serialize=json_output,
            rotation="5 MB",
            retention="7 days",
            backtrace=True,
            diagnose=debug,
        )

    logger.debug(
        "Logger initialized: debug=%s, json_output=%s, log_file=%s",
        debug,
        json_output,
        log_file,
    )


# app/core/logging.py
from app.core.config import settings


def setup_logger_from_settings():
    setup_logger(
        log_file="logs/nox.log",
        debug=settings.DEBUG,
        json_output=not settings.DEBUG,
    )
