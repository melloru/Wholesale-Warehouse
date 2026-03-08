from products.database.models import ProductCategory
from products.database.repositories import CategoryRepository
from products.application.schemas import CategoryCreateRequest


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository=repository)
