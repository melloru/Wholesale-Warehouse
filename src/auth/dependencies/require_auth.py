from uuid import UUID
from typing import Annotated

from fastapi import status
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession


from core.dependencies import (
    DbSession,
    UserServiceDep,
    SessionServiceDep,
)
from users.models import User
from auth.exceptions import AuthenticationError, TokenInvalidError
from auth.models import UserSession
from auth.schemas import TokenPayload
from auth.dependencies import TokenHelperDep


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
    except TokenInvalidError:
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
            session_id=UUID(payload.session_id),
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
