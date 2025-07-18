from loguru import logger

from app.core.logging import setup_logger


def test_logging_startup(caplog):
    setup_logger(debug=True)

    with caplog.at_level("INFO"):
        logger.info("Startup log test")

    assert "Startup log test" in caplog.text
