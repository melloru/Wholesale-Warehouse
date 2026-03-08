from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from auth.api.dependencies import get_auth_service, get_access_token_or_401
from auth.application.exceptions import (
    PermissionDeniedError,
    AuthenticationError,
    TokenInvalidError,
    SessionNotFoundError,
    SessionRevokedError,
    SessionExpiredError,
)
from auth.application.schemas import AccessTokenResponse, LoginSchema
from auth.application.services import AuthService, SessionService
from core.api.dependencies import (
    get_session,
    get_session_service,
    get_access_token,
    get_access_token_optional,
)
from core.infrastructure.database import db_helper

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[AuthService, Depends(get_auth_service)],
    login_data: LoginSchema,
):
    try:
        return await service.login(session, login_dto=login_data)
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/refresh", response_model=AccessTokenResponse | None)
async def refresh(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    access_token: Annotated[str, Depends(get_access_token)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await service.refresh(
            session,
            access_token=access_token,
        )
    except (
        TokenInvalidError,
        SessionNotFoundError,
        SessionRevokedError,
        SessionExpiredError,
    ) as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )


@router.post("/logout", response_model=None)
async def logout(
    session: Annotated[AsyncSession, Depends(get_session)],
    service: Annotated[AuthService, Depends(get_auth_service)],
    access_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(get_access_token_optional)
    ],
):
    return await service.logout(session, access_token=access_token.credentials)
