from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import UserSession
from auth.repositories import SessionRepository
from auth.schemas import SessionCreateRequest
from auth.exceptions import AuthenticationError
from auth.exceptions.session import (
    SessionNotFoundError,
    SessionRevokedError,
    SessionExpiredError,
)
from auth.exceptions.token import TokenInvalidError
from core.services import BaseService


class SessionService(BaseService[UserSession, SessionRepository, SessionCreateRequest]):
    def __init__(self, repository: SessionRepository):
        super().__init__(repository)

    async def revoke_session(
        self,
        session: AsyncSession,
        session_id: UUID,
    ) -> None:
        await self.repository.update_one(
            session,
            obj_id=session_id,
            **{"revoked": True},
        )

    async def get_valid_session(
        self,
        session: AsyncSession,
        session_id: UUID,
        jti: UUID,
    ) -> UserSession:
        user_session = await self.get_by_id(
            session,
            id=session_id,
        )
        if not user_session:
            raise SessionNotFoundError(message="Session not found")
        elif user_session.current_jti != jti:
            raise TokenInvalidError(message="Token is no longer valid")
        elif user_session.revoked:
            raise SessionRevokedError(message="Session revoked")
        elif datetime.now(timezone.utc) > user_session.exp:
            await self.revoke_session(session, session_id=session_id)
            raise SessionExpiredError(message="Session expired")

        return user_session

    async def get_session_if_valid(
        self,
        session: AsyncSession,
        session_id: UUID,
        jti: UUID,
    ) -> UserSession | None:
        try:
            return await self.get_valid_session(
                session,
                session_id=session_id,
                jti=jti,
            )
        except AuthenticationError:
            return None

    async def update_jti(
        self,
        session: AsyncSession,
        session_id: UUID,
        new_jti: UUID,
    ) -> None:
        await self.update_one(
            session,
            obj_id=session_id,
            **{"current_jti": new_jti},
        )
