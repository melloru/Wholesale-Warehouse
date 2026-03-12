import json

from redis.asyncio import Redis, ConnectionPool

from typing import Any

from core.config import config


class RedisConnectionManager:
    def __init__(
        self,
        max_connections: int = 20,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
    ):
        self.max_connections = max_connections
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout

        self.pool: ConnectionPool | None = ConnectionPool(
            host=config.redis.REDIS_HOST,
            port=config.redis.REDIS_PORT,
            db=config.redis.REDIS_DB,
            password=config.redis.REDIS_PASSWORD,
            decode_responses=True,
            encoding="utf-8",
            max_connections=self.max_connections,
            socket_connect_timeout=self.socket_connect_timeout,
            socket_timeout=self.socket_timeout,
            retry_on_timeout=True,
        )

    async def get(self, key: str) -> Any | None:
        async with Redis(connection_pool=self.pool) as conn:
            value = await conn.get(key)
            if value is None:
                return None
            return json.loads(value)

    async def set(
        self,
        key: str,
        ttl: int,
        value: Any,
    ) -> None:
        async with Redis(connection_pool=self.pool) as conn:
            await conn.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str) -> None:
        async with Redis(connection_pool=self.pool) as conn:
            await conn.delete(key)

    async def dispose(self) -> None:
        if self.pool:
            await self.pool.disconnect()
            self.pool = None


redis_manager = RedisConnectionManager(
    max_connections=config.redis.REDIS_MAX_CONNECTIONS,
)
