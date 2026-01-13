from datetime import datetime

from users.enums import UserStatus
from users.schemas.shared.base import BaseUser


class UserResponse(BaseUser):
    id: int
    email_verified: bool
    phone_verified: bool
    status: UserStatus
    is_staff: bool
    is_superadmin: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None


class UserDetailResponse(UserResponse):
    role_id: int
    is_deleted: bool
    deleted_at: datetime | None
