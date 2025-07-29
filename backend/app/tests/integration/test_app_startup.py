import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
# NOTE: Running this test in isolation may fail due to logs/nox.log permissions.
# Run with full test suite or ensure logs/ dir exists and is writable.
async def test_app_startup_and_shutdown_logs(caplog):
    caplog.set_level("INFO")

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/routers/health")
            assert response.status_code == 200
            assert response.json() == {"message": "OK"}

    startup_logged = any("starting up" in msg.lower() for msg in caplog.messages)
    shutdown_logged = any("shutting down" in msg.lower() for msg in caplog.messages)

    assert startup_logged, "Startup log message not found"
    assert shutdown_logged, "Shutdown log message not found"
