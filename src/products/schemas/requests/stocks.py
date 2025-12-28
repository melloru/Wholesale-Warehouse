from products.schemas.shared.base import BaseStock


class StockCreateRequest(BaseStock):
    product_id: int
