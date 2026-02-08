from datetime import datetime, timedelta
from jose import jwt
import secrets

SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token():
    return secrets.token_urlsafe(64)

def refresh_token_expiry():
    return datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
