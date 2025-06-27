import pytest
from argon2 import PasswordHasher

import app.core.security as security


@pytest.mark.parametrize(
    "password",
    [
        "StrongPass1!",
        "Another$Pass123",
        "Xyz@123abc",
        "Valid$Password9",
    ],
)
def test_check_password_valid(password):
    hashed = security.hash_password(password)
    assert security.check_password(password, hashed) is True


@pytest.mark.parametrize(
    "original_password,wrong_password",
    [
        ("StrongPass1!", "WrongPass1!"),
        ("Another$Pass123", "another$pass123"),  # lowercase variant
        ("Xyz@123abc", "Xyz@321abc"),  # swapped digits
        ("Valid$Password9", "Valid$Password99"),  # extra character
    ],
)
def test_check_password_invalid(original_password, wrong_password):
    hashed = security.hash_password(original_password)
    assert security.check_password(wrong_password, hashed) is False


@pytest.mark.parametrize(
    "password,broken_hash",
    [
        ("StrongPass1!", ""),  # Empty string
        ("StrongPass1!", "not-a-valid-hash"),  # Garbage string
        (
            "StrongPass1!",
            "$argon2id$v=19$m=65536,t=3,p=4$short$hash",
        ),  # Incomplete hash
        (
            "StrongPass1!",
            "$argon2id$v=19$m=65536,t=3,p=4$fakebase64$fakebase64",
        ),  # Valid format, nonsense content
        (
            "StrongPass1!",
            "$argon2id$v=19$m=65536,t=3,p=4$OOPS$this-was-edited",
        ),  # Tampered hash
    ],
)
def test_check_password_invalid_hash_format(password, broken_hash):
    assert security.check_password(password, broken_hash) is False


def test_needs_rehash_false_on_fresh_hash():
    password = "StrongPass1!"
    hashed = security.hash_password(password)

    assert security.needs_rehash(hashed) is False


def test_needs_rehash_true_on_weak_hash():
    # Simulate legacy hash with weaker settings
    weak_hasher = PasswordHasher(time_cost=1, memory_cost=8192, parallelism=1)
    weak_hash = weak_hasher.hash("StrongPass1!")

    assert security.needs_rehash(weak_hash) is True
