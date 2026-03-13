from pydantic import BaseModel
from users.api.schemas.base import BaseUser
from users.domain.enums import UserStatus


class UserPublicResponse(BaseUser):
    pass


class UserAdminResponse(UserPublicResponse):
    id: int
    email: str
    phone_number: str | None
    phone_verified: bool
    email_verified: bool
    role_id: int
    status: UserStatus


class UserCreatePublicResponse(BaseModel):
    id: int
