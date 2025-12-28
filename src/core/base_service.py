from typing import TypeVar, Generic, Sequence, Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Base
from core.database.base_repository import SqlalchemyRepository


T = TypeVar("T", bound=Base)
R = TypeVar("R", bound=SqlalchemyRepository)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)


class BaseService(Generic[T, R, CreateSchema]):
    """
    Базовый сервис для стандартных CRUD операций
    Args:
        T: Тип сущности (модель)
        R: Тип репозитория
        CreateSchema: Тип схемы создания сущности
    Attributes:
        repository (R): Репозиторий для доступа к данным
    """

    def __init__(self, repository: R):
        self.repository = repository

    async def get_by_id(
        self,
        session: AsyncSession,
        id: Any,
    ) -> T | None:
        return await self.repository.get_by_id(session, obj_id=id)

    async def get_one_or_none(
        self,
        session: AsyncSession,
        **filters,
    ) -> T | None:
        return await self.repository.get_one_or_none(session, **filters)

    async def get_many(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int | None = None,
        **filters,
    ) -> Sequence[T]:
        return await self.repository.get_many(
            session,
            skip=skip,
            limit=limit,
            **filters,
        )

    async def create(
        self,
        session: AsyncSession,
        obj_in: CreateSchema,
    ) -> T:
        return await self.repository.create(session, obj_in=obj_in)

    async def update_one(
        self,
        session: AsyncSession,
        obj_id: Any,
        **update_data,
    ) -> T | None:
        return await self.repository.update_one(
            session,
            obj_id=obj_id,
            **update_data,
        )
