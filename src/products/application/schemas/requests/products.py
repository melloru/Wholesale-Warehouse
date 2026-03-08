from products.application.schemas.shared.base import BaseProduct


class ProductCreateRequest(BaseProduct):
    category_id: int
