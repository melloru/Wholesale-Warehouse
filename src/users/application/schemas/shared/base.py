from pydantic import BaseModel, EmailStr

from users.application.schemas.shared.custom_types import NameStr, PublicNameStr


class BaseUser(BaseModel):
    email: EmailStr
    first_name: NameStr | None
    last_name: NameStr | None
    public_name: PublicNameStr | None
