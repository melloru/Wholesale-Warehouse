from products.models import ProductStock
from products.schemas import StockCreateDB
from core.database.base_repository import SqlalchemyRepository


class StockRepository(SqlalchemyRepository[ProductStock, StockCreateDB]):
    pass


def get_stock_repository() -> StockRepository:
    return StockRepository(ProductStock)
