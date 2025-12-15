from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.sessions import UserSession
from auth.repositories.session_repository import SessionRepository
from auth.schemas.session_schemas import SessionCreateRequest
from core.exceptions.session import (
    SessionNotFoundError,
    SessionRevokedError,
    SessionExpiredError,
)
from core.exceptions.token import TokenInvalidError
from core.services import BaseService


class SessionService(BaseService[UserSession, SessionRepository, SessionCreateRequest]):
    def __init__(self, repository: SessionRepository):
        super().__init__(repository)

    async def revoke_session(self, session: AsyncSession, id: UUID) -> None:
        await self.repository.update_one(session, obj_id=id, revoked=True)

    async def get_valid_session(
        self,
        session: AsyncSession,
        id: UUID,
        jti: UUID,
    ) -> UserSession:
        user_session = await self.get_by_id(session, id=id)
        if not user_session:
            raise SessionNotFoundError(message="Session not found")
        elif user_session.current_jti != jti:
            raise TokenInvalidError(message="Token is no longer valid")
        elif user_session.revoked:
            raise SessionRevokedError(message="Session revoked")
        elif datetime.now(timezone.utc) > user_session.expires_at:
            await self.revoke_session(session, id=id)
            raise SessionExpiredError(message="Session expired")

        return user_session

    # async def get_valid_session(
    #     self,
    #     session: AsyncSession,
    #     id: UUID,
    #     jti: UUID,
    # ) -> UserSession:
    #     user_session = await self.get_by_id(session, id=id)
    #     if not user_session:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Session not found",
    #         )
    #     elif user_session.current_jti != jti:
    #         await self.revoke_session(session, id=id)
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Token is no longer valid. Session revoked for protect",
    #         )
    #     elif user_session.revoked:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Session revoked",
    #         )
    #     elif datetime.now(timezone.utc) > user_session.expires_at:
    #         await self.revoke_session(session, id=id)
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Session expired",
    #         )
    #
    #     return user_session

    async def get_session_if_valid(
        self,
        session: AsyncSession,
        id: UUID,
        jti: UUID,
    ) -> UserSession | None:
        try:
            return await self.get_valid_session(
                session,
                id=id,
                jti=jti,
            )
        except HTTPException:
            return None
        except Exception:
            return None

    async def update_jti(
        self,
        session: AsyncSession,
        session_id: UUID,
        new_jti: UUID,
    ) -> UserSession | None:
        await self.update_one(
            session,
            obj_id=session_id,
            **{"current_jti": new_jti},
        )
