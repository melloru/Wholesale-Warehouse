from enum import Enum


class PermissionEnum(Enum):
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
    def all(cls) -> list["PermissionEnum"]:
        return list(cls)


class RoleEnum(Enum):
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
        self.permission_codes: tuple[PermissionEnum, ...] = ()

    @classmethod
    def all(cls) -> list["RoleEnum"]:
        """Все роли"""

        return list(cls)

    def permissions(self) -> tuple[PermissionEnum, ...]:
        """Разрешения роли (ленивая загрузка)"""

        if not self.permission_codes:
            self.permission_codes = self._get_permissions()
        return self.permission_codes

    def _get_permissions(self) -> tuple[PermissionEnum, ...]:
        """Получить разрешения для роли"""

        if self == RoleEnum.USER:
            return ()
        elif self == RoleEnum.SELLER:
            return (
                PermissionEnum.PRODUCT_CREATE,
                PermissionEnum.PRODUCT_EDIT_OWN,
                PermissionEnum.PRODUCT_DELETE_OWN,
                PermissionEnum.PRICE_EDIT_OWN,
                PermissionEnum.STOCK_EDIT_OWN,
            )
        elif self == RoleEnum.SUPER_ADMIN:
            return (
                PermissionEnum.PRODUCT_EDIT,
                PermissionEnum.PRODUCT_DELETE,
                PermissionEnum.PRODUCT_APPROVE,
                PermissionEnum.PRICE_EDIT,
                PermissionEnum.STOCK_EDIT,
                PermissionEnum.CATEGORY_EDIT,
                PermissionEnum.USER_EDIT,
                PermissionEnum.SELLER_APPROVE,
            )
        return ()
