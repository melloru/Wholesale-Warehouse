from core.base_service import BaseService
from products.models import ProductPrice
from products.schemas import PriceCreateRequest
from products.repositories import PriceRepository


class PriceService(
    BaseService[
        ProductPrice,
        PriceRepository,
        PriceCreateRequest,
    ]
):
    pass
