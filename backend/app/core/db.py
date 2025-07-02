from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Create the database engine
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Create a session factory
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


# Dependency injection for FastAPI routes/services
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
