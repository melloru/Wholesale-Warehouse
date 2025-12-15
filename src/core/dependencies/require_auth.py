from uuid import UUID
from typing import Annotated

from fastapi import Request, status
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.auth import AuthenticationError
from core.exceptions.token import TokenDecodeError
from auth.models.users import User
from auth.models.sessions import UserSession
from auth.schemas.token_schemas import TokenPayload
from core.dependencies import TokenHelperDep
from core.dependencies.database import DbSession
from core.dependencies.services import UserServiceDep, SessionServiceDep


async def get_access_token_or_401(
    token_result=Depends(
        HTTPBearer(auto_error=False)
    ),  # 👈 Используем стандартную схему
) -> str:
    """Получение токена с автоматической документацией"""
    if not token_result:
        raise HTTPException(401, "No access token provided")

    # token_result.credentials содержит сам токен
    return token_result.credentials


async def get_current_token_payload(
    token: Annotated[str | None, Depends(HTTPBearer(auto_error=False))],
    helper: TokenHelperDep,
) -> TokenPayload:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing",
        )
    try:
        payload = helper.decode_token(token, verify_exp=False)
    except TokenDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is empty",
        )

    return payload


async def get_current_session(
    session: DbSession,
    payload: Annotated[TokenPayload, Depends(get_current_token_payload)],
    service: SessionServiceDep,
) -> UserSession:
    try:
        return await service.get_valid_session(
            session,
            id=UUID(payload.session_id),
            jti=UUID(payload.jti),
        )
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )


async def get_current_user(
    session: AsyncSession,
    user_session: Annotated[UserSession, Depends(get_current_session)],
    service: UserServiceDep,
) -> User:
    user = await service.get_by_id(session, id=user_session.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


CurrentTokenPayload = Annotated[
    TokenPayload,
    Depends(get_current_token_payload),
]
CurrentSession = Annotated[
    UserSession,
    Depends(get_current_session),
]
CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]
