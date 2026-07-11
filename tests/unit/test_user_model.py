from app.models.user import User


def test_hash_password_returns_different_string():
    password = "correcthorse1"
    hashed = User.hash_password(password)
    assert hashed != password


def test_same_password_hashes_differently():
    password = "correcthorse1"
    assert User.hash_password(password) != User.hash_password(password)


def test_verify_password_accepts_correct_password():
    user = User(password_hash=User.hash_password("correcthorse1"))
    assert user.verify_password("correcthorse1") is True


def test_verify_password_rejects_wrong_password():
    user = User(password_hash=User.hash_password("correcthorse1"))
    assert user.verify_password("wronghorse") is False
