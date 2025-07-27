"""
Test fixtures for integration testing with FastAPI.

This module sets up:
- A test database (PostgreSQL URL modified from dev)
- Dependency overrides for DB access
- A test client with async support using httpx + FastAPI

Each test runs in a clean schema for isolation.
"""

import uuid
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.base import Base
from app.core.config import settings
from app.core.db import get_db
from app.core.limiting import limiter
from app.main import app

# Use a separate test database by replacing "_dev" with "_test"
TEST_DB_URL = str(settings.DATABASE_URL).replace("_dev", "_test")

# Use NullPool to avoid connection reuse across tests
engine_test = create_async_engine(TEST_DB_URL, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)


def unique_email():
    """
    Generates a unique dummy email address for testing.
    """
    return f"{uuid.uuid4().hex[:8]}@example.com"


def unique_username():
    """
    Generates a unique dummy username for testing.
    """
    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Required by pytest-anyio to specify the async backend.
    """
    return "asyncio"


@pytest.fixture(scope="function")
async def setup_test_db():
    """
    Creates all tables before each test and drops them after.

    Ensures schema isolation between test runs.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(setup_test_db):
    """
    Provides a test-scoped database session for use in tests.

    Depends on `setup_test_db` to ensure schema is initialized.
    """
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    """
    Provides an `httpx.AsyncClient` with overridden database dependencies.

    Allows full async HTTP testing with FastAPI endpoints and test DB.
    """

    app.dependency_overrides[get_db] = lambda: db_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
def reset_rate_limit():
    limiter.reset()


@pytest.fixture(autouse=True)
def disable_real_emails(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("app.services.onboarding.send_verification_email", mock)
    return mock  # optional: if you want to assert on it later
