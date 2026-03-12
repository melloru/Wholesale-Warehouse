from pydantic import BaseModel

from users.api.schemas.custom_types import NameStr, PublicNameStr


class BaseUser(BaseModel):
    first_name: NameStr | None = None
    last_name: NameStr | None = None
    public_name: PublicNameStr | None = None
