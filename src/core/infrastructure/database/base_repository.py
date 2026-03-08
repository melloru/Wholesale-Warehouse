from uuid import UUID
from dataclasses import asdict
from typing import TypeVar, Type, Any, Generic

from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.database.models import Base


EntityType = TypeVar("EntityType")
IdType = TypeVar("IdType", int, UUID, str)


class SqlalchemyRepository(Generic[EntityType, IdType]):
    """Базовый репозиторий"""

    def __init__(self, model: Type[Base], mapper):
        if not issubclass(model, Base):
            raise TypeError(f"Model {model} must inherit from Base")
        self.model = model
        self.mapper = mapper

    async def get_by_id(
        self,
        session: AsyncSession,
        obj_id: Any,
    ) -> EntityType | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        if not instance:
            return None
        return self.mapper.from_orm_to_entity(instance)

    async def get_one_or_none(
        self,
        session: AsyncSession,
        **filters,
    ) -> EntityType | None:
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        return self.mapper.from_orm_to_entity(instance)

    async def create(
        self,
        session: AsyncSession,
        entity: EntityType,
    ) -> EntityType:
        instance = self.model(**asdict(entity))
        session.add(instance)
        await session.flush()
        await session.refresh(instance)

        return self.mapper.from_orm_to_entity(instance)

    async def update(
        self,
        session: AsyncSession,
        entity: EntityType,
    ) -> EntityType:
        instance = await session.get(self.model, entity.id)

        if not instance:
            stmt = select(self.model).where(self.model.id == entity.id)
            result = await session.execute(stmt)
            instance = result.scalar_one()

        for key, value in asdict(entity).items():
            if key not in ('id', 'uuid') and hasattr(instance, key):
                current_value = getattr(instance, key)
                if current_value != value:
                    setattr(instance, key, value)

        await session.flush()
        await session.refresh(instance)
        return self.mapper.from_orm_to_entity(instance)
