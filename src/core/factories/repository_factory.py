from typing import Any

from users.models.users import User
from auth.models.user_sessions import UserSession
from users.repositories.user_repository import UserRepository
from auth.repositories.session_repository import SessionRepository


class RepositoryFactory:
    def __init__(self):
        self._cache: dict[str, Any] = {}

    def get_user_repository(self) -> UserRepository:
        if "user_repository" not in self._cache:
            self._cache["user_repository"] = UserRepository(User)
        return self._cache["user_repository"]

    def get_session_repository(self) -> SessionRepository:
        if "session_repository" not in self._cache:
            self._cache["session_repository"] = SessionRepository(UserSession)
        return self._cache["session_repository"]

    def clear(self):
        self._cache.clear()


repository_factory = RepositoryFactory()
