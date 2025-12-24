from typing import Any

from auth.helpers import PasswordHelper
from auth.helpers import TokenHelper


class HelperFactory:
    def __init__(self):
        self._cache: dict[str, Any] = {}

    def get_password_helper(self) -> PasswordHelper:
        if "password_hasher" not in self._cache:
            self._cache["password_hasher"] = PasswordHelper()
        return self._cache["password_hasher"]

    def get_token_helper(self) -> TokenHelper:
        if "token_service" not in self._cache:
            self._cache["token_service"] = TokenHelper()
        return self._cache["token_service"]

    def clear(self) -> None:
        self._cache.clear()


helper_factory = HelperFactory()
