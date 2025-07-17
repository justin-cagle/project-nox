"""
User service layer.

This module contains business logic related to user creation, including
password hashing and database interactions with proper error handling.
"""

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.messages import Registration
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(user_in: UserCreate, db: AsyncSession) -> User:
    """
    Creates a new user in the database with hashed credentials.

    Args:
        user_in (UserCreate): The data needed to create a new user.
        db (AsyncSession): Async database session for committing user data.

    Returns:
        User: The created user object from the database.

    Raises:
        HTTPException: If the user already exists (409 Conflict).
        SQLAlchemyError: For general database failures.
    """
    # Construct the user ORM model instance with hashed password.
    user = User(
        username=user_in.user_name,
        email=user_in.email,
        display_name=user_in.display_name,
        hashed_password=hash_password(user_in.password),
    )

    db.add(user)
    try:
        # Attempt to commit the new user to the database.
        await db.commit()
    except IntegrityError:
        # Likely caused by a duplicate username or email.
        print(">>> Caught IntegrityError")
        await db.rollback()
        raise HTTPException(status_code=409, detail=Registration.DUPE_USER)
    except SQLAlchemyError as e:
        # Roll back on any unexpected DB error.
        print(">>> Caught SQLAlchemyError:", e)
        await db.rollback()
        raise

    # Refresh to ensure the returned object has any DB-assigned fields populated (e.g., id).
    await db.refresh(user)
    return user
