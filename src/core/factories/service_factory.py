from typing import Any

from users.services import UserService
from auth.services import SessionService, AuthService
from products.services import (
    ProductService,
    CategoryService,
    StockService,
    PriceService,
)
from core.factories import (
    HelperFactory,
    RepositoryFactory,
    helper_factory,
    repository_factory,
)


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

    def get_product_service(self) -> ProductService:
        if "product_service" not in self._cache:
            self._cache["product_service"] = ProductService(
                repository=self._repository_factory.get_product_repository()
            )
        return self._cache["product_service"]

    def get_category_service(self) -> CategoryService:
        if "category_service" not in self._cache:
            self._cache["category_service"] = CategoryService(
                repository=self._repository_factory.get_category_repository()
            )
        return self._cache["category_service"]

    def get_stock_service(self) -> StockService:
        if "stock_service" not in self._cache:
            self._cache["stock_service"] = StockService(
                repository=self._repository_factory.get_stock_repository()
            )
        return self._cache["stock_service"]

    def get_price_service(self) -> PriceService:
        if "price_service" not in self._cache:
            self._cache["price_service"] = PriceService(
                repository=self._repository_factory.get_price_repository()
            )
        return self._cache["price_service"]

    def clear(self):
        self._cache.clear()


service_factory = ServiceFactory(
    repository_factory=repository_factory,
    helper_factory=helper_factory,
)
