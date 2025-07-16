"""
Alembic migration environment setup.

Responsibilities:
- Load SQLAlchemy `Base.metadata` for autogeneration
- Load `.env` for DB connection string (ALEMBIC_DATABASE_URL)
- Support both offline and online migration modes
"""

import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context
from app import models  # noqa F401 - Silence "import not used" complaint
from app.core.base import Base  # Import your metadata here

# Alembic Config object (from alembic.ini)
config = context.config

# Load logging config if available
if config.config_file_name:
    fileConfig(config.config_file_name)

# Load .env file one level up (project root)
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

# Load DB URL from environment
db_url = os.getenv("ALEMBIC_DATABASE_URL")
if not db_url:
    raise RuntimeError("Missing ALEMBIC_DATABASE_URL in .env file.")
config.set_main_option("sqlalchemy.url", db_url)

# Metadata for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run Alembic migrations in 'offline' mode (SQL script output)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run Alembic migrations in 'online' mode (direct DB connection)."""
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


# Entrypoint: choose offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
