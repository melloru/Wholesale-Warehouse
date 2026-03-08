from core.base_service import BaseService
from products.database.models import ProductPrice
from products.application.schemas import PriceCreateRequest
from products.database.repositories import PriceRepository


class PriceService(
    BaseService[
        ProductPrice,
        PriceRepository,
        PriceCreateRequest,
    ]
):
    def __init__(self, repository: PriceRepository):
        super().__init__(repository=repository)

    async def get_prices_for_product(self):
        pass
