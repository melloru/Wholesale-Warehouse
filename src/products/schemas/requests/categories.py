from products.schemas.shared.base import BaseCategory


class CategoryCreateRequest(BaseCategory):
    parent_id: int
