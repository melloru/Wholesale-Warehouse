from typing import Any

from users.services.user_service import UserService
from auth.services.auth_service import AuthService
from auth.services.session_service import SessionService
from core.factories.helper_factory import HelperFactory, helper_factory
from core.factories.repository_factory import RepositoryFactory, repository_factory


class ServiceFactory:
    def __init__(
        self,
        repository_factory: RepositoryFactory,
        helper_factory: HelperFactory,
    ):
        self._cache: dict[str, Any] = {}
        self._repository_factory = repository_factory
        self._helper_factory = helper_factory

    def get_user_service(self) -> UserService:
        if "user_service" not in self._cache:
            self._cache["user_service"] = UserService(
                repository=self._repository_factory.get_user_repository(),
                password_helper=self._helper_factory.get_password_helper(),
            )
        return self._cache["user_service"]

    def get_session_service(self) -> SessionService:
        if "session_service" not in self._cache:
            self._cache["session_service"] = SessionService(
                repository=self._repository_factory.get_session_repository(),
            )
        return self._cache["session_service"]

    def get_auth_service(self) -> AuthService:
        if "auth_service" not in self._cache:
            self._cache["auth_service"] = AuthService(
                user_service=self.get_user_service(),
                session_service=self.get_session_service(),
                token_helper=self._helper_factory.get_token_helper(),
                password_helper=self._helper_factory.get_password_helper(),
            )
        return self._cache["auth_service"]

    def clear(self):
        self._cache.clear()


service_factory = ServiceFactory(
    repository_factory=repository_factory,
    helper_factory=helper_factory,
)
