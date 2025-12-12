from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.users import User
from auth.repositories.user_repository import UserRepository
from auth.schemas.user_schemas import UserCreateRequest, UserCreateDB
from auth.helpers.password_helper import PasswordHelper
from core.services import BaseService


class UserService(BaseService[User, UserRepository, UserCreateRequest]):
    def __init__(
        self,
        repository: UserRepository,
        password_helper: PasswordHelper,
    ):
        super().__init__(repository)
        self.password_hasher = password_helper

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User:
        return await super().get_one_or_none(session, email=email)

    async def create(
        self,
        session: AsyncSession,
        new_user_data: UserCreateRequest,
    ) -> User:
        password_hash = self.password_hasher.hash_password(new_user_data.password)
        user_db = UserCreateDB(
            **new_user_data.model_dump(exclude={"password"}),
            password_hash=password_hash,
        )
        new_user = await self.repository.create(session, obj_in=user_db)
        return new_user
