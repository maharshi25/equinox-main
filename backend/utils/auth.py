import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_ALGORITHM = "HS256"
security_scheme = HTTPBearer(auto_error=False)


def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    env_name = os.getenv("ENV", "development").lower()

    if secret:
        if len(secret) < 32:
            raise RuntimeError("JWT_SECRET_KEY must be at least 32 characters long for HS256")
        return secret

    if env_name in {"development", "dev", "test", "testing"}:
        return "local-dev-secret-key-for-equinox-1234567890"

    raise RuntimeError("JWT_SECRET_KEY environment variable must be set in production environments")


JWT_SECRET_KEY = _get_jwt_secret()


def create_access_token(email: str, expires_delta_seconds: int = 60 * 60 * 12) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email.lower(),
        "iat": now,
        "exp": now + timedelta(seconds=expires_delta_seconds),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise ValueError("Invalid or expired JWT token") from exc

    email = payload.get("sub")
    if not email:
        raise ValueError("JWT payload is missing the user email")

    return str(email).lower()


async def get_current_user_email(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
