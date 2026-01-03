from core.base_service import BaseService
from products.models import Product
from products.schemas import ProductCreateRequest
from products.repositories import ProductRepository


class ProductService(
    BaseService[
        Product,
        ProductRepository,
        ProductCreateRequest,
    ]
):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository=repository)
