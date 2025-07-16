"""
Shared declarative base class for SQLAlchemy models.

All ORM models in the project should inherit from `Base`
to ensure consistent metadata and reflection support.
"""

from sqlalchemy.orm import declarative_base

# Unified base class for all SQLAlchemy ORM models
Base = declarative_base()
