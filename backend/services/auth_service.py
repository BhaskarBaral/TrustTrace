"""Module: services/auth_service.py"""
import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from services.user_service import get_user_by_email, verify_password

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "trusttrace-dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
