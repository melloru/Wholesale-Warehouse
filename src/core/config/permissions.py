from enum import Enum


class PermissionEnum(Enum):
    """Enum для прав доступа"""

    LEAVE_REVIEW = ("review_create", "Создание отзывов")
    ANSWER_REVIEW_OWN = ("review_answer_own", "Ответить на свой отзыв")

    PRODUCT_CREATE = ("product_create", "Создать товар")
    PRODUCT_EDIT_OWN = ("product_edit_own", "Изменить свой товар")
    PRODUCT_DELETE_OWN = ("product_delete_own", "Удалить свой товар")
    PRICE_EDIT_OWN = ("price_edit_own", "Настроить цену своего товара")
    STOCK_EDIT_OWN = ("stock_edit_own", "Обновить кол-во своего товара")

    ADMIN_PANEL = ("admin_panel", "Админ панель")

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
            return (PermissionEnum.ADMIN_PANEL,)
        return ()
