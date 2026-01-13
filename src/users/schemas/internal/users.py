from pydantic import Field

from core.config.permissions import RoleEnum
from users.enums import UserStatus
from users.schemas.shared.base import BaseUser


class UserCreateDB(BaseUser):
    password_hash: str
    role_id: int = Field(default=RoleEnum.USER.id)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_superadmin: bool = Field(default=False)
