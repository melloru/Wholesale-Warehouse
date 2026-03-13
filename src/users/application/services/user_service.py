from sqlalchemy.ext.asyncio import AsyncSession

from core.config.permissions import RoleEnum
from users.api.schemas.requests import (
    UserCreatePublicRequest,
    UserUpdatePublicRequest,
    UserCreateAdminRequest,
    UserUpdateAdminRequest,
)

from users.application.exceptions import UserAlreadyExistsError
from users.domain.enums import UserStatus
from users.infrastructure.cache.cache_user_repository import CachedUserRepository
from users.infrastructure.helpers import PasswordHelper
from users.infrastructure.exceptions import UserIntegrityError
from users.infrastructure.database.repositories import UserRepository
from users.domain.entities import UserEntity


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_helper: PasswordHelper,
        cached_user_repository: CachedUserRepository,
    ):
        self.user_repository = user_repository
        self.password_helper = password_helper
        self.cached_user_repository = cached_user_repository

    async def create(
        self,
        session: AsyncSession,
        create_data: UserCreatePublicRequest | UserCreateAdminRequest,
    ) -> UserEntity:
        password_hash = self.password_helper.hash_password(
            plain_password=create_data.password_plain
        )

        user_entity = UserEntity(
            id=None,
            email=create_data.email,
            password_hash=password_hash,
            phone_number=create_data.phone_number,
            first_name=create_data.first_name,
            last_name=create_data.last_name,
            public_name=create_data.public_name,
            role_id=getattr(create_data, "role_id", RoleEnum.USER.id),
            status=getattr(create_data, "status", UserStatus.PENDING),
            phone_verified=getattr(create_data, "phone_verified", False),
            email_verified=getattr(create_data, "email_verified", False),
        )
        try:
            return await self.user_repository.create(session, entity=user_entity)
        except UserIntegrityError as e:
            raise UserAlreadyExistsError("User with this email already exists") from e

    async def get_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserEntity | None:

        return await self.cached_user_repository.get_by_id(
            session,
            user_id=user_id,
        )

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserEntity | None:
        return await self.cached_user_repository.get_by_email(
            session,
            email=email,
        )

    async def update(
        self,
        session: AsyncSession,
        user_id: int,
        update_data: UserUpdatePublicRequest | UserUpdateAdminRequest,
    ) -> UserEntity:
        user_entity = await self.cached_user_repository.get_by_id(
            session,
            user_id=user_id,
        )
        old_email = user_entity.email
        update_dict = update_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        user_entity.update(data=update_dict)
        updated_user_entity = await self.user_repository.update(
            session,
            entity=user_entity,
        )
        await self.cached_user_repository.invalidate(
            user_id=user_id,
            email=old_email if "email" in update_dict else None,
        )
        return updated_user_entity
