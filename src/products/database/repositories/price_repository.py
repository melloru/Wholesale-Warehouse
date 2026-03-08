from products.database.models import ProductPrice
from products.application.schemas import PriceCreateDB
from core.infrastructure.database.base_repository import SqlalchemyRepository


class PriceRepository(
    SqlalchemyRepository[
        ProductPrice,
        PriceCreateDB,
    ]
):
    pass
