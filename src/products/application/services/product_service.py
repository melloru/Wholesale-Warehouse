from core.base_service import BaseService
from products.database.models import Product
from products.application.schemas import ProductCreateRequest
from products.database.repositories import ProductRepository


class ProductService(
    BaseService[
        Product,
        ProductRepository,
        ProductCreateRequest,
    ]
):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository=repository)
