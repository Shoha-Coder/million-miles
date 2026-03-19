from fastapi import APIRouter, HTTPException, status

from src.application.use_cases.login import Login
from src.config import settings
from src.domain.exceptions import InvalidCredentials
from src.presentation.dependencies import SessionDep, create_token
from src.presentation.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(_session: SessionDep, body: LoginRequest) -> TokenResponse:
    use_case = Login(
        valid_username=settings.admin_username,
        valid_password=settings.admin_password,
    )
    try:
        await use_case.execute(body.username, body.password)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )

    return TokenResponse(access_token=create_token(body.username))
