from pydantic import BaseModel
from users.application.schemas.shared.base import BaseUser


class UserPublicResponse(BaseUser):
    pass


class UserCreatePublicResponse(BaseModel):
    id: int
