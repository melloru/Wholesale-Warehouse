from sqlalchemy.ext.asyncio import AsyncSession

from products.services import (
    ProductService,
    CategoryService,
    StockService,
    PriceService,
)


class ProductManagerService:
    """Агрегированный сервис для управления товарами (используется в админских и seller роутерах)"""

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

    async def create_product_with_details(self, session: AsyncSession):
        """Создать товар со всеми связанными данными"""
        pass

    async def update_product_full(self, product_id, updates):
        """Обновить товар и связанные данные"""
        pass
