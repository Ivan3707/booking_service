import pytest
from src.auth.jwt import create_access_token, decode_token


def test_jwt_encode_decode():
    token = create_access_token({
        "user_id": "123",
        "role": "user"
    })

    payload = decode_token(token)

    assert payload["user_id"] == "123"
    assert payload["role"] == "user"