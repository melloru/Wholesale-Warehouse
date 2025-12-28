from products.models import Product
from products.schemas import ProductCreateDB
from core.database.base_repository import SqlalchemyRepository


class ProductRepository(SqlalchemyRepository[Product, ProductCreateDB]):
    pass


def get_product_repository() -> ProductRepository:
    return ProductRepository(Product)
