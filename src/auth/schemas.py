from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, EmailStr, StringConstraints, Field

from auth.enums import UserRole, UserStatus


PUBLIC_NAME_PATTERN = r"^[a-zA-Z0-9_\-\.]+$"
PASSWORD_PATTERN = r"^[a-zA-Z0-9!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]+$"
NAME_PATTERN = r"^[a-zA-Zа-яА-ЯёЁ'\-\s]+$"
PHONE_PATTERN = r"^\+?[1-9]\d{1,14}$"

PublicNameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=50,
        pattern=PUBLIC_NAME_PATTERN,
    ),
]

NameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=100,
        pattern=NAME_PATTERN,
    ),
]

PasswordStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=128,
        pattern=PASSWORD_PATTERN,
    ),
]

PhoneStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=PHONE_PATTERN,
    ),
]


class BaseUser(BaseModel):
    email: EmailStr
    first_name: NameStr | None
    last_name: NameStr | None
    public_name: PublicNameStr | None
    phone_number: PhoneStr | None


class UserSchema(BaseUser):
    id: int
    email_verified: bool
    phone_verified: bool
    role: UserRole
    status: UserStatus
    is_staff: bool
    is_superadmin: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None


class UserDetailSchema(UserSchema):
    permissions: dict[str, Any]
    is_deleted: bool
    deleted_at: datetime | None


class CreateUserSchema(BaseUser):
    password_hash: PasswordStr
    role: UserRole = Field(
        default=UserRole.CUSTOMER,
    )


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
