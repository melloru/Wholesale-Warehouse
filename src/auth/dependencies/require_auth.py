from uuid import UUID
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
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
from auth.exceptions import AuthenticationError, TokenInvalidError


async def get_current_token_payload(
    token: Annotated[str | None, Depends(HTTPBearer(auto_error=False))],
    helper: Annotated[TokenHelper, Depends(helper_factory.get_token_helper())],
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
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    payload: Annotated[TokenPayload, Depends(get_current_token_payload)],
    service: Annotated[SessionService, Depends(service_factory.get_session_service)],
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
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user_session: Annotated[UserSession, Depends(get_current_session)],
    service: Annotated[UserService, Depends(service_factory.get_user_service)],
) -> User:
    user = await service.get_by_id(session, id=user_session.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
