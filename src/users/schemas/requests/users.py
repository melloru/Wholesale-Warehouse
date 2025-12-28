from users.schemas.shared.base import BaseUser
from users.schemas.shared.custom_types import PasswordStr


class UserCreateRequest(BaseUser):
    password: PasswordStr
