from redis.asyncio import Redis, ConnectionPool
from redis.asyncio.client import Pipeline
from redis.exceptions import RedisError

from typing import AsyncGenerator

from core.config import config


class RedisHelper:
    def __init__(
        self,
        max_connections: int = 20,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
    ):
        self.max_connections = max_connections
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout

        self.pool: ConnectionPool = ConnectionPool(
            host=config.redis.REDIS_HOST,
            port=config.redis.REDIS_PORT,
            db=config.redis.REDIS_DB,
            password=config.redis.REDIS_PASSWORD,
            ssl=config.redis.REDIS_SSL,
            decode_responses=True,
            encoding="utf-8",
            max_connections=self.max_connections,
            socket_connect_timeout=self.socket_connect_timeout,
            socket_timeout=self.socket_timeout,
            retry_on_timeout=True,
        )

    async def get_client(self) -> AsyncGenerator[Redis, None]:
        async with Redis(connection_pool=self.pool) as client:
            yield client

    async def get_pipeline_client(
        self,
        transaction: bool = False,
    ) -> AsyncGenerator[Pipeline, None]:
        """Контекст для MULTI/EXEC операций"""
        async for client in self.get_client():
            pipe = client.pipeline(transaction=transaction)
            try:
                yield pipe
                await pipe.execute()
            except RedisError:
                if transaction:
                    await pipe.reset()
                raise

    def get_watched_client(
        self,
        watch_keys: list[str] | None = None,
        with_pipeline: bool = False,
        transaction: bool = True,
    ):
        pass

    async def dispose(self):
        if self.pool:
            await self.pool.disconnect()
            self.pool = None


redis_helper = RedisHelper(
    max_connections=config.REDIS_MAX_CONNECTIONS,
)
