from enum import Enum


class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    BANNED = "banned"


class CurrencyCode(Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    CNY = "CNY"
