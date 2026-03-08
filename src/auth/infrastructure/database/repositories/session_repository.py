from typing import Type
from uuid import UUID

from sqlalchemy.sql import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.entities import UserSessionEntity
from auth.infrastructure.session_mapper import SessionMapper
from core.infrastructure.database.base_repository import SqlalchemyRepository
from auth.infrastructure.database.models import UserSession


class SessionRepository:
    def __init__(
        self,
        model: Type[UserSession],
        mapper: SessionMapper,
    ):
        self.model = model
        self.mapper = mapper
        self.base_repository: SqlalchemyRepository[UserSessionEntity, UUID] = (
            SqlalchemyRepository(
                model=model,
                mapper=mapper,
            )
        )

    async def create(
        self,
        session: AsyncSession,
        session_entity: UserSessionEntity,
    ) -> UserSessionEntity:
        return await self.base_repository.create(
            session,
            entity=session_entity,
        )

    async def get_by_id(
        self,
        session: AsyncSession,
        session_id: UUID,
    ) -> UserSessionEntity:
        return await self.base_repository.get_by_id(
            session,
            obj_id=session_id,
        )

    async def update(
        self,
        session,
        session_entity: UserSessionEntity,
    ) -> UserSessionEntity:
        return await self.base_repository.update(
            session,
            entity=session_entity,
        )

    async def update_jti(
        self,
        session: AsyncSession,
        session_id: UUID,
        new_jti: UUID,
    ) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == session_id)
            .values(current_jti=new_jti)
        )
        await session.execute(stmt)
