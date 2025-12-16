from core.database.repositories import SqlalchemyRepository
from auth.models import User
from auth.schemas import UserCreateDB


class UserRepository(SqlalchemyRepository[User, UserCreateDB]):
    pass


def get_user_repository() -> UserRepository:
    return UserRepository(User)
