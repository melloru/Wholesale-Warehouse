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
    pass
