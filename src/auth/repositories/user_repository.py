from core.database.repositories import SqlalchemyRepository
from auth.models.users import User
from auth.schemas.user_schemas import UserCreateDB


class UserRepository(SqlalchemyRepository[User, UserCreateDB]):
    pass


def get_user_repository() -> UserRepository:
    return UserRepository(User)
