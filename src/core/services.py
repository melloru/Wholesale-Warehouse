from typing import TypeVar, Generic, Sequence

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base
from core.repositories import SqlalchemyRepository


T = TypeVar("T", bound=Base)
R = TypeVar("R", bound=SqlalchemyRepository)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)


class BaseService(Generic[T, R, CreateSchema]):
    def __init__(self, repository: R):
        self.repository = repository

    async def get_by_id(self, session: AsyncSession, id: int) -> T | None:
        return await self.repository.get_by(session, id=id)

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
