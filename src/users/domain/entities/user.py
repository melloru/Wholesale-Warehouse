from dataclasses import dataclass

from core.config.permissions import RoleEnum
from users.domain.enums import UserStatus


@dataclass
class UserEntity:
    id: int | None
    email: str
    password_hash: str
    first_name: str | None
    last_name: str | None
    public_name: str | None
    phone_number: str | None
    phone_verified: bool = False
    email_verified: bool = False
    role_id: int = RoleEnum.USER.id
    status: UserStatus = UserStatus.PENDING
