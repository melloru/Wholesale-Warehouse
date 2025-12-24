from typing import Annotated

from fastapi.params import Depends

from core.factories.service_factory import service_factory
from users.services.user_service import UserService
from auth.services.auth_service import AuthService
from auth.services.session_service import SessionService


def get_user_service() -> UserService:
    return service_factory.get_user_service()


def get_session_service() -> SessionService:
    return service_factory.get_session_service()


def get_auth_service() -> AuthService:
    return service_factory.get_auth_service()


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
