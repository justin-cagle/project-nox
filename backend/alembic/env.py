import os
from logging.config import fileConfig

# Load .env for DB connection URL
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context

# Load SQLAlchemy metadata
from app.core.base import Base

# Alembic Config object
config = context.config

# Setup loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Look one level above the alembic/ folder
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=dotenv_path)

# Override sqlalchemy.url with value from .env
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Metadata for 'autogenerate' support
target_metadata = Base.metadata


# --- OFFLINE mode ---
def run_migrations_offline() -> None:
    """Run migrations without a live DB connection (DDL only)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- ONLINE mode (sync engine only) ---
def run_migrations_online() -> None:
    """Run migrations with a sync engine to avoid async inspection bugs."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Entrypoint ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
