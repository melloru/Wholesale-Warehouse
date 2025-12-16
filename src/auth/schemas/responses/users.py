from typing import Any
from datetime import datetime

from auth.enums import UserRole, UserStatus
from auth.schemas.shared.base import BaseUser


class UserResponse(BaseUser):
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


class UserDetailResponse(UserResponse):
    permissions: dict[str, Any]
    is_deleted: bool
    deleted_at: datetime | None
