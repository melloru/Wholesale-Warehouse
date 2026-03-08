from sqlalchemy.ext.asyncio import AsyncSession

from users.application.schemas import UserCreateRequest
from users.application.exceptions import UserNotFoundError, UserAlreadyExistsError
from users.infrastructure.helpers import PasswordHelper
from users.infrastructure.exceptions import UserIntegrityError
from users.infrastructure.database.repositories import UserRepository
from users.domain.entities import UserEntity


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_helper: PasswordHelper,
    ):
        self.user_repository = user_repository
        self.password_helper = password_helper

    async def get_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserEntity | None:
        user_entity = await self.user_repository.get_by_id(
            session,
            user_id=user_id,
        )
        if not user_entity:
            raise UserNotFoundError(f"User with id {user_id} not found")

        return user_entity

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserEntity | None:
        return await self.user_repository.get_one_or_none(
            session,
            email=email,
        )

    async def create(
        self,
        session: AsyncSession,
        user_data: UserCreateRequest,
    ) -> UserEntity:
        password_hash = self.password_helper.hash_password(
            plain_password=user_data.password_plain
        )

        user_entity = UserEntity(
            id=None,
            email=user_data.email,
            password_hash=password_hash,
            phone_number=user_data.phone_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            public_name=user_data.public_name,
        )
        try:
            return await self.user_repository.create(session, entity=user_entity)
        except UserIntegrityError as e:
            raise UserAlreadyExistsError("User with this email already exists") from e
