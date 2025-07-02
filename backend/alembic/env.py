from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

# Load SQLAlchemy metadata
from app.core.base import Base

# Alembic Config object
config = context.config

# Setup loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


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
