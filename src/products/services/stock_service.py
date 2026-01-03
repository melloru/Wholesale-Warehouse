from core.base_service import BaseService
from products.models import ProductStock
from products.schemas import StockCreateRequest
from products.repositories import StockRepository


class StockService(
    BaseService[
        ProductStock,
        StockRepository,
        StockCreateRequest,
    ]
):
    def __init__(self, repository: StockRepository):
        super().__init__(repository=repository)

    async def get_stock_for_product(self):
        pass
