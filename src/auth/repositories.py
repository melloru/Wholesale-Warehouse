from typing import TYPE_CHECKING, Type, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories import SqlalchemyRepository
from auth.models import User


class UserRepository(SqlalchemyRepository[User]):
    pass


def get_user_repository() -> UserRepository:
    return UserRepository(User)
