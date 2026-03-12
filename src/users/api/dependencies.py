from core.infrastructure.cache import redis_manager
from core.infrastructure.cache.keys import UserCacheKeyPattern
from users.infrastructure.cache.cache_user_repository import CachedUserRepository
from users.infrastructure.database.models import User
from users.infrastructure.helpers import PasswordHelper
from users.application.services import UserService
from users.infrastructure.database.repositories import UserRepository
from users.infrastructure.user_mapper import UserMapper


def get_user_service() -> UserService:
    user_repository = UserRepository(
        model=User,
        mapper=UserMapper(),
    )
    return UserService(
        user_repository=user_repository,
        password_helper=PasswordHelper(),
        cached_user_repository=CachedUserRepository(
            user_repository=user_repository,
            redis_manager=redis_manager,
            key_pattern=UserCacheKeyPattern(),
        ),
    )
