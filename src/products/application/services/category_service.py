from products.database.repositories import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository=repository)
