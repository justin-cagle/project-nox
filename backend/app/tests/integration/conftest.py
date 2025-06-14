import pytest
import pytest_asyncio

# from app.core.db import \
# get_session  # You will need to define or adjust this dependency
from app.core.db import Base
from app.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# from sqlalchemy.orm import sessionmaker

# Use a file-based SQLite test DB for now (more stable than in-memory for initial tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

# Create sessionmaker bound to test engine
AsyncSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

transport = ASGITransport(app=app)


# Override the app's dependency to use test session
async def override_get_session() -> AsyncSession:
    print("Creating tables on test engine:", test_engine)
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Create test DB schema before any tests run.
    """
    # Force import all models so they are registered with Base.metadata
    #    import app.models.user

    print("Creating tables on test engine:", test_engine)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Optional: drop tables after tests (clean up)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(prepare_database):
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
