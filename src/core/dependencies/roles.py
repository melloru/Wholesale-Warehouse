from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from auth.models.users import User
from core.dependencies.require_auth import CurrentUser


def admin_only(user: CurrentUser) -> User:
    if not user.is_superadmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


AdminOnly = Annotated[User, Depends(admin_only)]
