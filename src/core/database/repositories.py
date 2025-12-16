from typing import TypeVar, Generic, Type, Sequence, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.database.models import Base


T = TypeVar("T", bound=Base)
TCreate = TypeVar("TCreate", bound=BaseModel)


class SqlalchemyRepository(Generic[T, TCreate]):
    def __init__(self, model: Type[T]):
        if not issubclass(model, Base):
            raise TypeError(f"Model {model} must inherit from Base")
        self.model = model

    async def get_by_id(
        self,
        session: AsyncSession,
        obj_id: Any,
    ) -> T | None:
        stmt = select(self.model).filter_by(id=obj_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_one_or_none(
        self,
        session: AsyncSession,
        **filters,
    ) -> T | None:
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_first(
        self,
        session: AsyncSession,
        **filters,
    ) -> T | None:
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)

        return result.scalars().first()

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
        obj_in: TCreate,
    ) -> T:
        data = obj_in.model_dump(exclude_unset=True)

        instance = self.model(**data)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)

        return instance

    async def update_one(
        self,
        session: AsyncSession,
        obj_id: Any,
        **update_data,
    ) -> None:
        stmt = update(self.model).where(self.model.id == obj_id).values(**update_data)

        await session.execute(stmt)
        await session.flush()
