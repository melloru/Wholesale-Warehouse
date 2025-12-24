from uuid import UUID
from typing import Annotated

from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import DbSession, SessionServiceDep, UserServiceDep
from users.models import User
from auth.models import UserSession
from auth.schemas import TokenPayload
from auth.dependencies import TokenHelperDep
from auth.exceptions import TokenInvalidError


async def get_maybe_token_payload(
    token: Annotated[str | None, Depends(HTTPBearer(auto_error=False))],
    helper: TokenHelperDep,
) -> TokenPayload | None:
    if not token:
        return None
    try:
        return helper.decode_token(token, verify_exp=False)
    except TokenInvalidError:
        return None


async def get_maybe_session(
    session: DbSession,
    payload: Annotated[TokenPayload | None, Depends(get_maybe_token_payload)],
    service: SessionServiceDep,
) -> UserSession | None:
    if not payload:
        return None

    return await service.get_session_if_valid(
        session,
        session_id=UUID(payload.session_id),
        jti=UUID(payload.jti),
    )


async def get_maybe_user(
    session: AsyncSession,
    user_session: Annotated[UserSession | None, Depends(get_maybe_session)],
    service: UserServiceDep,
) -> User | None:
    if not user_session:
        return None

    return await service.get_by_id(session, id=user_session.user_id)


MaybeTokenPayload = Annotated[
    TokenPayload | None,
    Depends(get_maybe_token_payload),
]
MaybeSession = Annotated[
    UserSession | None,
    Depends(get_maybe_session),
]
MaybeUser = Annotated[
    User | None,
    Depends(),
]
