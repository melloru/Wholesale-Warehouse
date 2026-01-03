from sqlalchemy.ext.asyncio import AsyncSession

from products.services import (
    ProductService,
    CategoryService,
    StockService,
    PriceService,
)


class ProductCatalogService:
    """Для получения/отображения товаров в каталоге"""

    def __init__(
        self,
        product_service: ProductService,
        category_service: CategoryService,
        stock_service: StockService,
        price_service: PriceService,
    ):
        self.product_service = product_service
        self.category_service = category_service
        self.stock_service = stock_service
        self.price_service = price_service

    async def get_catalog_product(self, session: AsyncSession, product_id: int):
        pass

    async def get_catalog_page(self, session: AsyncSession):
        pass
