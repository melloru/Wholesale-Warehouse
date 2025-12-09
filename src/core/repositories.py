from typing import TypeVar, Generic, Type, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.models import Base


T = TypeVar("T", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)


class SqlalchemyRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        if not issubclass(model, Base):
            raise TypeError(f"Model {model} must inherit from Base")
        self.model = model

    async def get_by(
        self,
        session: AsyncSession,
        **filters,
    ) -> T | None:
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_many(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int | None = None,
        **filters,
    ) -> Sequence[T]:
        stmt = select(self.model).filter_by(**filters)

        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)

        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        obj_in: CreateSchema,
    ) -> T:
        data = obj_in.model_dump(exclude_unset=True)

        instance = self.model(**data)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)

        return instance
