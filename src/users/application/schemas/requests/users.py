from users.application.schemas.shared.base import BaseUser
from users.application.schemas.shared.custom_types import PasswordStr, PhoneStr


class UserCreateRequest(BaseUser):
    phone_number: PhoneStr | None
    password_plain: PasswordStr
