import hashlib

from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions

hasher = PasswordHasher(
    time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16
)


def hash_password(password: str) -> str:
    return hasher.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    try:
        return hasher.verify(hashed_password, password)
    except (
        argon2_exceptions.VerifyMismatchError,
        argon2_exceptions.VerificationError,
        argon2_exceptions.InvalidHashError,
    ):
        return False


def needs_rehash(hashed: str) -> bool:
    return hasher.check_needs_rehash(hashed)


def hash_str(string: str, purpose: str | None = None) -> str:
    if purpose is not None:
        input_str = f"{purpose}:{string}"
    else:
        input_str = string

    encoded = hashlib.sha256(input_str.encode("utf-8"))

    return encoded.hexdigest()
