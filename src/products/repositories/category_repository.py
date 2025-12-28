from products.models import ProductCategory
from products.schemas import CategoryCreateDB
from core.database.base_repository import SqlalchemyRepository


class CategoryRepository(SqlalchemyRepository[ProductCategory, CategoryCreateDB]):
    pass
