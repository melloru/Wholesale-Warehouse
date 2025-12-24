from pydantic import Field

from users.enums import UserRole
from users.schemas.shared.base import BaseUser
from users.schemas.shared.types import PasswordStr


class UserCreateRequest(BaseUser):
    password: PasswordStr
    role: UserRole = Field(
        default=UserRole.CUSTOMER,
    )
