from products.database.models import ProductCategory
from products.application.schemas import CategoryCreateDB
from core.infrastructure.database.base_repository import SqlalchemyRepository


class CategoryRepository(
    SqlalchemyRepository[
        ProductCategory,
        CategoryCreateDB,
    ]
):
    pass
