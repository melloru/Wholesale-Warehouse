from pydantic import EmailStr

from users.api.schemas.base import BaseUser
from users.api.schemas.custom_types import PasswordStr, PhoneStr
from users.domain.enums import UserStatus


class UserCreatePublicRequest(BaseUser):
    """
    Запрос на создание нового пользователя

    Этот DTO используется при регистрации нового пользователя в системе
    Все поля проходят валидацию перед отправкой в сервисный слой

    Кто может использовать: Все

    Пример:
        {
            "email": "user@example.com",
            "password_plain": "SecurePass123",
            "first_name": "Иван",
            "last_name": "Петров",
            "public_name": "Иван Петров",
            "phone_number": "+375291234567"
        }
    """

    email: EmailStr
    phone_number: PhoneStr | None
    password_plain: PasswordStr


class UserCreateAdminRequest(UserCreatePublicRequest):
    """
    Запрос на создание нового пользователя
    Поля проходят валидацию перед отправкой в сервисный слой

    Кто может использовать: Админ
    Пример:
        {
            "email": "user@example.com",
            "password_plain": "SecurePass123",
            "first_name": "Иван",
            "last_name": "Петров",
            "public_name": "Иван Петров",
            "phone_number": "+375291234567"
        }
    """

    role_id: int
    status: UserStatus
    phone_verified: bool = False
    email_verified: bool = False


class UserUpdatePublicRequest(BaseUser):
    email: EmailStr | None = None
    plain_password: PasswordStr | None = None


class UserUpdateAdminRequest(UserUpdatePublicRequest):
    role_id: int | None = None
    status: UserStatus | None = None
    phone_verified: bool | None = None
    email_verified: bool | None = None
    is_deleted: bool | None = None
