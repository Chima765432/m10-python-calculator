import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User


def make_user(username="alice", email="alice@example.com"):
    return User(
        username=username,
        email=email,
        password_hash=User.hash_password("longenough1"),
    )


def test_user_is_stored_and_read_back(db_session):
    db_session.add(make_user())
    db_session.commit()
    stored = db_session.query(User).filter_by(username="alice").one()
    assert stored.email == "alice@example.com"
    assert stored.id is not None
    assert stored.created_at is not None


def test_duplicate_username_is_rejected(db_session):
    db_session.add(make_user())
    db_session.commit()
    db_session.add(make_user(email="other@example.com"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_duplicate_email_is_rejected(db_session):
    db_session.add(make_user())
    db_session.commit()
    db_session.add(make_user(username="bob"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_stored_hash_verifies_original_password(db_session):
    db_session.add(make_user())
    db_session.commit()
    stored = db_session.query(User).filter_by(username="alice").one()
    assert stored.verify_password("longenough1") is True
