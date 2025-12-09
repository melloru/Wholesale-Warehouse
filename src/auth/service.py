from auth.models import User
from auth.repositories import UserRepository, get_user_repository
from auth.schemas import CreateUserSchema
from core.services import BaseService


class UserService(BaseService[User, UserRepository, CreateUserSchema]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)


def get_user_service() -> UserService:
    return UserService(get_user_repository())
