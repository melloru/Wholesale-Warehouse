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
    pass
