from typing import Annotated

from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.users import User
from auth.models.sessions import UserSession
from auth.schemas.token_schemas import TokenPayloadInternal
from core.dependencies.helpers import TokenHelperDep
from core.dependencies.database import DbSession
from core.dependencies.services import SessionServiceDep, UserServiceDep


async def get_maybe_token_payload(
    token: Annotated[str, Depends(HTTPBearer(auto_error=False))],
    helper: TokenHelperDep,
) -> TokenPayloadInternal | None:
    if not token:
        return None
    try:
        return helper.decode_token(token)
    except Exception:
        return None


async def get_maybe_session(
    session: DbSession,
    payload: Annotated[TokenPayloadInternal | None, Depends(get_maybe_token_payload)],
    service: SessionServiceDep,
) -> UserSession | None:
    if not payload:
        return None

    session_id = payload.get("session_id")
    if not session_id:
        return None

    return await service.get_session_if_valid(session, id=session_id)


async def get_maybe_user(
    session: AsyncSession,
    user_session: Annotated[UserSession | None, Depends(get_maybe_session)],
    service: UserServiceDep,
) -> User | None:
    if not user_session:
        return None

    return await service.get_by_id(session, id=user_session.user_id)


MaybeTokenPayload = Annotated[
    TokenPayloadInternal | None,
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
