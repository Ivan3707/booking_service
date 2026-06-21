import os
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def create_access_token(payload: dict, expires_minutes: int = 60):
    data = payload.copy()
    data["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])