from products.database.models import ProductStock
from products.application.schemas import StockCreateDB
from core.infrastructure.database.base_repository import SqlalchemyRepository


class StockRepository(
    SqlalchemyRepository[
        ProductStock,
        StockCreateDB,
    ]
):
    pass
