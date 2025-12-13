from typing import Annotated

from fastapi import status
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.users import User
from auth.models.sessions import UserSession
from auth.schemas.token_schemas import TokenPayloadInternal
from core.dependencies.database import DbSession
from core.dependencies.services import UserServiceDep, SessionServiceDep
from core.dependencies.optional_auth import MaybeTokenPayload


async def get_current_token_payload(
    payload: MaybeTokenPayload,
) -> TokenPayloadInternal:
    if not payload:
        raise HTTPException(status_code=401, detail="Authentication required")
    return payload


async def get_current_session(
    session: DbSession,
    payload: Annotated[TokenPayloadInternal, Depends(get_current_token_payload)],
    service: SessionServiceDep,
) -> UserSession:
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no session ID",
        )

    return await service.get_valid_session(session, id=session_id)


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
    TokenPayloadInternal,
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
