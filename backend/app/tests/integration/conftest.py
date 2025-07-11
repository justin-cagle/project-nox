"""
Test fixtures for integration testing with FastAPI.

This module sets up:
- A test database (PostgreSQL URL modified from dev)
- Dependency overrides for DB access
- A test client with async support using httpx + FastAPI

Each test runs in a clean schema for isolation.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.base import Base
from app.core.config import settings
from app.core.db import get_db
from app.main import app

# Use a separate test database by replacing "_dev" with "_test"
TEST_DB_URL = str(settings.DATABASE_URL).replace("_dev", "_test")

# Use NullPool to avoid connection reuse across tests
engine_test = create_async_engine(TEST_DB_URL, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)


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

    # Override FastAPI's get_db dependency with the test session
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
