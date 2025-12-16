from pydantic import Field

from auth.enums import UserRole
from auth.schemas.shared.base import BaseUser
from auth.schemas.shared.types import PasswordStr


class UserCreateRequest(BaseUser):
    password: PasswordStr
    role: UserRole = Field(
        default=UserRole.CUSTOMER,
    )
