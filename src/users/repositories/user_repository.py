from core.database.base_repository import SqlalchemyRepository
from users.models import User
from users.schemas import UserCreateDB


class UserRepository(SqlalchemyRepository[User, UserCreateDB]):
    pass
