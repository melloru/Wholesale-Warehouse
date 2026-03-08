from users.infrastructure.database.models import User
from users.infrastructure.helpers import PasswordHelper
from users.application.services import UserService
from users.infrastructure.database.repositories import UserRepository
from users.infrastructure.user_mapper import UserMapper


def get_user_service() -> UserService:
    return UserService(
        user_repository=UserRepository(
            model=User,
            mapper=UserMapper(),
        ),
        password_helper=PasswordHelper(),
    )
