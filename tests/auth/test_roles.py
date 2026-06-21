import pytest
from fastapi import HTTPException
from src.auth.dependencies import require_user, require_admin


def test_require_user_ok():
    user = {"user_id": "1", "role": "user"}
    assert require_user(user) == user


def test_require_user_fail():
    user = {"user_id": "1", "role": "admin"}

    try:
        require_user(user)
        assert False
    except HTTPException as e:
        assert e.status_code == 403


def test_require_admin_ok():
    user = {"user_id": "1", "role": "admin"}
    assert require_admin(user) == user


def test_require_admin_fail():
    user = {"user_id": "1", "role": "user"}

    try:
        require_admin(user)
        assert False
    except HTTPException as e:
        assert e.status_code == 403