from typing import Any

from users.models import User
from auth.models import UserSession
from products.models import Product, ProductCategory, ProductStock, ProductPrice
from users.repositories import UserRepository
from auth.repositories import SessionRepository
from products.repositories import (
    ProductRepository,
    CategoryRepository,
    StockRepository,
    PriceRepository,
)


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

    def get_product_repository(self) -> ProductRepository:
        if "product_repository" not in self._cache:
            self._cache["product_repository"] = ProductRepository(model=Product)
        return self._cache["product_repository"]

    def get_category_repository(self) -> CategoryRepository:
        if "category_repository" not in self._cache:
            self._cache["category_repository"] = CategoryRepository(
                model=ProductCategory
            )
        return self._cache["category_repository"]

    def get_stock_repository(self) -> StockRepository:
        if "stock_repository" not in self._cache:
            self._cache["stock_repository"] = StockRepository(model=ProductStock)
        return self._cache["stock_repository"]

    def get_price_repository(self) -> PriceRepository:
        if "price_repository" not in self._cache:
            self._cache["price_repository"] = PriceRepository(model=ProductPrice)
        return self._cache["price_repository"]

    def clear(self):
        self._cache.clear()


repository_factory = RepositoryFactory()
