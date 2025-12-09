from core.repositories import SqlalchemyRepository
from auth.models import User


class UserRepository(SqlalchemyRepository[User]):
    pass


def get_user_repository() -> UserRepository:
    return UserRepository(User)
