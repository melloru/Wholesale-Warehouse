from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.base_repository import SqlalchemyRepository
from users.domain.entities import UserEntity
from users.infrastructure.database.models import User
from users.infrastructure.exceptions import UserIntegrityError
from users.infrastructure.user_mapper import UserMapper


class UserRepository:
    def __init__(
        self,
        model: Type[User],
        mapper: UserMapper,
    ) -> None:
        self.model = model
        self.mapper = mapper
        self.base_repository = SqlalchemyRepository[UserEntity, int](
            model=model,
            mapper=mapper,
        )

    async def create(
        self,
        session: AsyncSession,
        entity: UserEntity,
    ) -> UserEntity:
        try:
            return await self.base_repository.create(
                session,
                entity=entity,
            )
        except IntegrityError as e:
            raise UserIntegrityError("Conflict when adding user") from e

    async def get_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserEntity | None:
        return await self.base_repository.get_by_id(
            session,
            obj_id=user_id,
        )

    async def get_one_or_none(
        self,
        session: AsyncSession,
        **filters,
    ) -> UserEntity | None:
        return await self.base_repository.get_one_or_none(
            session,
            **filters,
        )

    async def update(
        self,
        session,
        entity: UserEntity,
    ) -> UserEntity:
        return await self.base_repository.update(
            session,
            entity=entity,
        )
