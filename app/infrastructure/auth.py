import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status

SECRET_KEY = "your_secret_key"  # Replace with a secure key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360  # 6 hours


def create_access_token(data: dict):
    """Generate a JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except PyJWTError as e:
        print(f"Token verification error: {e}")  # Debug
        raise HTTPException(status_code=401, detail="Invalid token")
