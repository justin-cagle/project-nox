"""
Alembic migration environment setup.

This script configures Alembic's context for running schema migrations,
including database URL resolution from `.env`, metadata loading, and both
offline/online migration modes.

Key responsibilities:
- Load SQLAlchemy `Base.metadata` for autogeneration
- Load `.env` file to pull a database connection string
- Support both offline (SQL output) and online (live DB) migration modes
"""

import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context
from app.core.base import Base

# Alembic Config object (from alembic.ini)
config = context.config

# Load logging config if present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load .env one directory up (e.g., root/.env)
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=dotenv_path)

# Read DB URL from environment (.env preferred over alembic.ini)
db_url = os.getenv("ALEMBIC_DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# This is what Alembic uses for `autogenerate` to detect model changes
target_metadata = Base.metadata


# --- OFFLINE mode ---
def run_migrations_offline() -> None:
    """
    Run Alembic migrations in 'offline' mode.

    Generates SQL script without connecting to a live database.
    Useful for code review or auditing changes before applying.
    """
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


# --- ONLINE mode ---
def run_migrations_online() -> None:
    """
    Run Alembic migrations in 'online' mode using a sync SQLAlchemy engine.

    Connects directly to the target database and applies migrations.
    Sync engine avoids async reflection bugs with certain dialects.
    """
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


# Entrypoint: choose offline or online based on CLI context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
