from typing import Annotated, AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.services import TokenService
from auth.application.exceptions import (
    TokenInvalidError,
    TokenExpiredError,
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
)
from auth.application.services import SessionService
from core.config.permissions import RoleEnum
from core.infrastructure.database.db_helper import db_helper
from users.infrastructure.helpers import PasswordHelper
from users.api.dependencies import get_user_service
from users.application.services import UserService
from users.domain.entities import UserEntity
from auth.infrastructure.database.models import UserSession
from auth.infrastructure.database.repositories import SessionRepository
from auth.infrastructure.session_mapper import SessionMapper


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.get_session():
        yield session


def get_token_service() -> TokenService:
    return TokenService()


def get_password_helper() -> PasswordHelper:
    return PasswordHelper()


def get_access_token_optional(
    access_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))
    ],
) -> str | None:
    if access_token is None:
        return None

    elif access_token.scheme != "Bearer":
        raise HTTPException(
            status_code=401,
            detail="Incorrect token scheme",
        )

    return access_token.credentials


def get_access_token(
    access_token: Annotated[str | None, Depends(get_access_token_optional)],
) -> str:
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Token missing",
        )
    return access_token


def get_session_service() -> SessionService:
    return SessionService(
        session_repository=SessionRepository(
            model=UserSession,
            mapper=SessionMapper(),
        ),
        token_helper=get_token_service(),
    )


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    session_service: Annotated[SessionService, Depends(get_session_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    access_token: Annotated[str, Depends(get_access_token)],
) -> UserEntity:
    try:
        payload = token_service.decode_token(
            token=access_token,
            expected_type="access",
        )
    except (TokenExpiredError, TokenInvalidError) as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

    try:
        session_entity = await session_service.get_valid_session(
            session,
            session_id=UUID(payload.session_id),
            jti=UUID(payload.jti),
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
    user_entity = await user_service.get_by_id(
        session,
        user_id=session_entity.user_id,
    )
    return user_entity


async def get_admin(
    user_entity: Annotated[UserEntity, Depends(get_current_user)],
) -> UserEntity:
    if user_entity.role_id == RoleEnum.SUPER_ADMIN.id:
        return user_entity
    raise HTTPException(
        status_code=403,
        detail="Admin privileges required",
    )
