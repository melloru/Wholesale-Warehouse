from products.database.models import Product
from products.application.schemas import ProductCreateDB
from core.infrastructure.database.base_repository import SqlalchemyRepository


class ProductRepository(
    SqlalchemyRepository[
        Product,
        ProductCreateDB,
    ]
):
    pass
