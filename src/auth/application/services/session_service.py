from dataclasses import asdict
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.schemas import (
    TokenCreate,
    SessionCreateInternal,
)
from auth.domain.entities import UserSessionEntity
from auth.infrastructure.database.models import UserSession
from auth.infrastructure.database.repositories import SessionRepository
from auth.application.exceptions import (
    AuthenticationError,
    SessionNotFoundError,
    SessionRevokedError,
    SessionExpiredError,
    TokenInvalidError,
)
from auth.application.services import TokenService
from core.infrastructure.database import db_helper


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository,
        token_helper: TokenService,
    ):
        self.session_repository = session_repository
        self.token_helper = token_helper

    async def create(
        self,
        session: AsyncSession,
        session_dto: SessionCreateInternal,
    ):
        session_entity = UserSessionEntity(**session_dto.model_dump())

        return await self.session_repository.create(
            session,
            session_entity=session_entity,
        )

    async def get_valid_session(
        self,
        session: AsyncSession,
        session_id: UUID,
        jti: UUID,
    ) -> UserSessionEntity | None:
        session_entity = await self.session_repository.get_by_id(
            session,
            session_id=session_id,
        )
        if not session_entity:
            raise SessionNotFoundError("Session not found")
        elif session_entity.revoked:
            raise SessionRevokedError("Session revoked")
        elif datetime.now(timezone.utc) > session_entity.exp:
            async for nested_session in db_helper.get_session():
                session_entity.revoked = True
                session_entity.revoke_reason = "Session expired"
                await self.session_repository.update(
                    nested_session,
                    session_entity=session_entity,
                )
            raise SessionExpiredError("Session expired")
        elif session_entity.current_jti != jti:
            raise TokenInvalidError("Incorrect JTI")

        return session_entity

    async def revoke_session(
        self,
        session: AsyncSession,
        session_id: UUID,
    ) -> None:
        session_entity = await self.session_repository.get_by_id(
            session,
            session_id=session_id,
        )
        session_entity.revoked = True

        await self.session_repository.update(
            session,
            session_entity=session_entity,
        )

    async def update_jti(
        self,
        session: AsyncSession,
        session_id: UUID,
        new_jti: UUID,
    ) -> None:
        await self.session_repository.update_jti(
            session,
            session_id=session_id,
            new_jti=new_jti,
        )
