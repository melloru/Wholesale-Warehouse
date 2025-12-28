from core.base_service import BaseService
from products.models import ProductCategory
from products.repositories import CategoryRepository
from products.schemas import CategoryCreateRequest


class CategoryService(
    BaseService[
        ProductCategory,
        CategoryRepository,
        CategoryCreateRequest,
    ]
):
    pass
