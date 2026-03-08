from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.application.services import AuthService
from core.api.dependencies import (
    get_token_service,
    get_password_helper,
    get_session_service,
)
from users.api.dependencies import get_user_service


async def get_access_token_or_401(
    token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))
    ],
) -> str:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="No access token provided",
        )

    return token.credentials


def get_auth_service():
    return AuthService(
        user_service=get_user_service(),
        session_service=get_session_service(),
        token_service=get_token_service(),
        password_helper=get_password_helper(),
    )
