"""
Security utilities for password and string hashing.

This module includes:
- Argon2-based password hashing and verification
- Rehash detection logic
- SHA256 hashing for general-purpose tokens (e.g. reuse prevention)
"""

import hashlib

from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions

# Argon2 hasher instance with tuned security parameters
hasher = PasswordHasher(
    time_cost=3,  # Number of iterations (CPU cost)
    memory_cost=65536,  # Memory usage in KB
    parallelism=4,  # Number of parallel threads
    hash_len=32,  # Length of resulting hash
    salt_len=16,  # Random salt length
)


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using Argon2id.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password string (includes salt and metadata).
    """
    return hasher.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a previously hashed one.

    Args:
        password (str): The input plaintext password.
        hashed_password (str): The stored hash to verify against.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    try:
        return hasher.verify(hashed_password, password)
    except (
        argon2_exceptions.VerifyMismatchError,
        argon2_exceptions.VerificationError,
        argon2_exceptions.InvalidHashError,
    ):
        return False


def needs_rehash(hashed: str) -> bool:
    """
    Checks whether the password hash needs to be rehashed based on current params.

    Args:
        hashed (str): The stored hash string.

    Returns:
        bool: True if rehashing is recommended, False if still valid.
    """
    return hasher.check_needs_rehash(hashed)


def hash_str(string: str, purpose: str | None = None) -> str:
    """
    Generates a deterministic SHA256 hash for a string.

    Used for hashing token strings for storage without reversibility.

    Args:
        string (str): The input string to hash.
        purpose (str, optional): If provided, prepends a namespace for salt-like separation.

    Returns:
        str: A hex-encoded SHA256 hash of the input.
    """
    if purpose is not None:
        input_str = f"{purpose}:{string}"
    else:
        input_str = string

    encoded = hashlib.sha256(input_str.encode("utf-8"))
    return encoded.hexdigest()
