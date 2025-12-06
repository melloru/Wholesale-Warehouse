from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import config

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine: "AsyncEngine" = create_async_engine(url, echo=echo)
        self.session_factory = async_sessionmaker(
            self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_getter(self):
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


db_helper = DatabaseHelper(
    url=config.db.db_url,
    echo=config.db.POSTGRES_ECHO,
)
