import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserRead


def test_user_create_accepts_valid_data():
    user = UserCreate(username="alice", email="alice@example.com", password="longenough1")
    assert user.username == "alice"


def test_user_create_rejects_bad_email():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="not-an-email", password="longenough1")


def test_user_create_rejects_short_password():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="alice@example.com", password="short")


def test_user_create_rejects_short_username():
    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="alice@example.com", password="longenough1")


def test_user_read_has_no_password_fields():
    assert "password" not in UserRead.model_fields
    assert "password_hash" not in UserRead.model_fields
