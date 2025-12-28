from products.models import ProductPrice
from products.schemas import PriceCreateDB
from core.database.base_repository import SqlalchemyRepository


class PriceRepository(SqlalchemyRepository[ProductPrice, PriceCreateDB]):
    pass


def get_price_repository() -> PriceRepository:
    return PriceRepository(ProductPrice)
