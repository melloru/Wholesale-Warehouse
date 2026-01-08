from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class Permission(Enum):
    """Enum для прав доступа"""

    PRODUCT_CREATE = ("product:create", "Создание новых товаров")
    PRODUCT_EDIT_OWN = ("product:edit_own", "Изменение своих товаров")
    PRODUCT_DELETE_OWN = ("product:delete_own", "Удаление своих товаров")
    PRICE_EDIT_OWN = ("price:edit_own", "Настройка цен своих товаров")
    STOCK_EDIT_OWN = ("stock:edit_own", "Обновление кол-ва своего товара")

    PRODUCT_EDIT = ("product:edit", "Изменение любых товаров")
    PRODUCT_DELETE = ("product:delete", "Удаление любых товаров")
    PRODUCT_APPROVE = ("product:approve", "Одобрение товаров")
    PRICE_EDIT = ("price:edit", "Настройка любых цен")
    STOCK_EDIT = ("stock:edit", "Управление остатками")
    CATEGORY_EDIT = ("category:edit", "Редактирование категорий")
    USER_EDIT = ("user:edit", "Редактирование пользователей")
    SELLER_APPROVE = ("user:approve", "Одобрение продавцов")

    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description

    @classmethod
    def all(cls) -> list["Permission"]:
        return list(cls)


class Role(Enum):
    """Роль с ID, именем и описанием"""

    USER = (1, "user", "Покупатель/клиент")
    SELLER = (2, "seller", "Продавец товаров")
    SUPER_ADMIN = (3, "super_admin", "Супер администратор")

    def __init__(
        self,
        id: int,
        role_name: str,
        description: str,
    ):
        self.id = id
        self.role_name = role_name
        self.description = description
        self.permission_codes: tuple[Permission, ...] = ()

    @classmethod
    def all(cls) -> list["Role"]:
        """Все роли"""

        return list(cls)

    def permissions(self) -> tuple[Permission, ...]:
        """Разрешения роли (ленивая загрузка)"""

        if not self.permission_codes:
            self.permission_codes = self._get_permissions()
        return self.permission_codes

    def _get_permissions(self) -> tuple[Permission, ...]:
        """Получить разрешения для роли"""

        if self == Role.USER:
            return ()
        elif self == Role.SELLER:
            return (
                Permission.PRODUCT_CREATE,
                Permission.PRODUCT_EDIT_OWN,
                Permission.PRODUCT_DELETE_OWN,
                Permission.PRICE_EDIT_OWN,
                Permission.STOCK_EDIT_OWN,
            )
        elif self == Role.SUPER_ADMIN:
            return (
                Permission.PRODUCT_EDIT,
                Permission.PRODUCT_DELETE,
                Permission.PRODUCT_APPROVE,
                Permission.PRICE_EDIT,
                Permission.STOCK_EDIT,
                Permission.CATEGORY_EDIT,
                Permission.USER_EDIT,
                Permission.SELLER_APPROVE,
            )
        return ()
