import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token


def test_password_hashing_and_verification():
    """Sprawdza, czy zahaszowane hasło jest poprawnie weryfikowane."""
    password = "SuperSecret123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_pass", hashed) is False


def test_password_hashes_are_unique():
    """Upewnia się, że to samo hasło daje różne hasze (dzięki soli)."""
    password = "test"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    assert hash1 != hash2


def test_create_access_token_contains_correct_data():
    """Weryfikuje, czy wygenerowany token zawiera poprawne dane sub (username)."""
    username = "admin_user"
    token = create_access_token(subject=username)

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == username
    assert "exp" in payload