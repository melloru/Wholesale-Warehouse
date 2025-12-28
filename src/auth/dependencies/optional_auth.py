from uuid import UUID
from typing import Annotated

from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db_helper import db_helper
from core.factories import helper_factory, service_factory
from users.models import User
from auth.models import UserSession
from auth.schemas import TokenPayload
from users.services import UserService
from auth.services import SessionService
from auth.helpers import TokenHelper
from auth.exceptions import TokenInvalidError


async def get_maybe_token_payload(
    token: Annotated[str | None, Depends(HTTPBearer(auto_error=False))],
    helper: Annotated[TokenHelper, Depends(helper_factory.get_token_helper)],
) -> TokenPayload | None:
    if not token:
        return None
    try:
        return helper.decode_token(token, verify_exp=False)
    except TokenInvalidError:
        return None


async def get_maybe_session(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    payload: Annotated[TokenPayload | None, Depends(get_maybe_token_payload)],
    service: Annotated[SessionService, Depends(service_factory.get_session_service)],
) -> UserSession | None:
    if not payload:
        return None

    return await service.get_session_if_valid(
        session,
        session_id=UUID(payload.session_id),
        jti=UUID(payload.jti),
    )


async def get_maybe_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user_session: Annotated[UserSession | None, Depends(get_maybe_session)],
    service: Annotated[UserService, Depends(service_factory.get_user_service)],
) -> User | None:
    if not user_session:
        return None

    return await service.get_by_id(session, id=user_session.user_id)
