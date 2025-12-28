from products.schemas.shared.base import BasePrice


class PriceCreateRequest(BasePrice):
    product_id: int
