from pydantic import BaseModel, Field

from products.schemas.shared.custom_types import NameStr


class BaseProduct(BaseModel):
    """Базовая схема с общими полями продукта"""

    name: NameStr
    description: str | None
    weight_kg: float | None


class BasePrice(BaseModel):
    """Базовая схема с общими полями цен продукта"""

    price_per_unit_minor: int
    min_quantity: int


class BaseStock(BaseModel):
    """Базовая схема с общими полями кол-ва продукта"""

    available_quantity: int
    is_on_demand: bool


class BaseCategory(BaseModel):
    """Базовая схема с общими полями категории продукта"""

    name: str
    sort_order: int = Field(default=0)
    description: str | None
