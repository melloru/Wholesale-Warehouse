from pydantic import Field

from users.enums import UserRole, UserStatus
from users.schemas.shared.base import BaseUser


class UserCreateDB(BaseUser):
    password_hash: str
    role: UserRole = Field(default=UserRole.CUSTOMER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_superadmin: bool = Field(default=False)
