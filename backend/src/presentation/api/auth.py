from fastapi import APIRouter, HTTPException, status

from src.application.use_cases.login import Login
from src.config import settings
from src.domain.exceptions import InvalidCredentials
from src.presentation.dependencies import (
    RefreshDep,
    SessionDep,
    create_access_token,
    create_refresh_token,
)
from src.presentation.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _token_pair(username: str) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(username),
        refresh_token=create_refresh_token(username),
    )


@router.post("/login", response_model=TokenResponse)
async def login(_session: SessionDep, body: LoginRequest) -> TokenResponse:
    use_case = Login(
        valid_username=settings.admin_username,
        valid_password_hash=settings.admin_password_hash,
        extra_username=settings.admin_username_2,
        extra_password_hash=settings.admin_password_hash_2,
    )
    try:
        username = await use_case.execute(body.username, body.password)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )
    return _token_pair(username)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(username: RefreshDep) -> TokenResponse:
    # Rotate both tokens on every refresh — old refresh token is implicitly invalidated
    return _token_pair(username)
