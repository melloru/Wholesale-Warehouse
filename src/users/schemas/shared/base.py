from pydantic import BaseModel, EmailStr

from users.schemas.shared.types import NameStr, PublicNameStr, PhoneStr


class BaseUser(BaseModel):
    email: EmailStr
    first_name: NameStr | None
    last_name: NameStr | None
    public_name: PublicNameStr | None
    phone_number: PhoneStr | None
