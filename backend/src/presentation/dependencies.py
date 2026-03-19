from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.infrastructure.database.base import get_session

_bearer = HTTPBearer()

# Access tokens are short-lived; refresh tokens carry the long-lived session
ACCESS_TOKEN_EXPIRE_MINUTES  = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days


def _make_token(username: str, expire_minutes: int, kind: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    return jwt.encode(
        {"sub": username, "exp": expire, "typ": kind},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(username: str) -> str:
    return _make_token(username, ACCESS_TOKEN_EXPIRE_MINUTES, "access")


def create_refresh_token(username: str) -> str:
    return _make_token(username, REFRESH_TOKEN_EXPIRE_MINUTES, "refresh")


def _decode(token: str, expected_kind: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if payload.get("typ") != expected_kind:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token type")
        username: str | None = payload.get("sub")
        if not username:
            raise JWTError("missing sub")
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_auth(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> str:
    return _decode(credentials.credentials, "access")


def require_refresh(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> str:
    return _decode(credentials.credentials, "refresh")


SessionDep = Annotated[AsyncSession, Depends(get_session)]
AuthDep    = Annotated[str, Depends(require_auth)]
RefreshDep = Annotated[str, Depends(require_refresh)]
