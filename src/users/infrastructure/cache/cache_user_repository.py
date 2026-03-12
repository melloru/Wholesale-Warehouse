from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.cache import RedisConnectionManager
from core.infrastructure.cache.keys import UserCacheKeyPattern
from users.domain.entities import UserEntity
from users.infrastructure.database.repositories import UserRepository


class CachedUserRepository:
    def __init__(
        self,
        user_repository: UserRepository,
        redis_manager: RedisConnectionManager,
        key_pattern: UserCacheKeyPattern,
    ):
        self.user_repository = user_repository
        self.redis_manager = redis_manager
        self.key_pattern = key_pattern

    async def get_by_id(self, session: AsyncSession, user_id: int) -> UserEntity | None:
        key = self.key_pattern.USER_BY_ID.format(user_id=user_id)
        value: dict = await self.redis_manager.get(key)
        if value is not None:
            return UserEntity(**value)

        user_entity = await self.user_repository.get_by_id(
            session,
            user_id=user_id,
        )
        if user_entity is not None:
            await self.redis_manager.set(
                key=key,
                ttl=300,
                value=asdict(user_entity),
            )

        return user_entity

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserEntity | None:
        email_key = self.key_pattern.USER_ID_BY_EMAIL.format(email=email)
        if user_id := await self.redis_manager.get(key=email_key):
            return await self.get_by_id(session, user_id=user_id)

        user_entity = await self.user_repository.get_by_email(
            session,
            email=email,
        )
        if user_entity is not None:
            await self.redis_manager.set(
                key=self.key_pattern.USER_BY_ID.format(user_id=user_entity.id),
                ttl=300,
                value=asdict(user_entity),
            )
            await self.redis_manager.set(
                key=email_key,
                ttl=300,
                value=user_entity.id,
            )

        return user_entity

    async def invalidate(
        self,
        user_id: int,
        email: str | None = None,
    ) -> None:
        await self.redis_manager.delete(
            self.key_pattern.USER_BY_ID.format(user_id=user_id)
        )
        if email:
            await self.redis_manager.delete(
                self.key_pattern.USER_ID_BY_EMAIL.format(email=email)
            )
