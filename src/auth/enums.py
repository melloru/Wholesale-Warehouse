from enum import Enum


class UserRole(Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    MEDIATOR = "mediator"


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    BANNED = "banned"
