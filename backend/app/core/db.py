"""
Database connection and session management.

This module defines the SQLAlchemy async engine and session factory using
environment-provided settings. It also includes a `get_db` dependency that
FastAPI routes can use to access a scoped database session.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Create the database engine using asyncpg and the configured DATABASE_URL
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Create a session factory bound to the engine
# `expire_on_commit=False` prevents SQLAlchemy from expiring ORM objects
# after commits, allowing them to be reused in the same request.
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


# Dependency injection function for FastAPI routes/services
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async SQLAlchemy session.

    Yields:
        AsyncSession: An async session for use in DB operations.
    """
    async with async_session() as session:
        yield session
