from sqlalchemy import (
    Enum,
    BigInteger,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base
from core.database.mixins import TimestampMixin
from products.enums import CurrencyCode


class ProductPrice(Base, TimestampMixin):
    __tablename__ = "product_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    price_per_unit_minor: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Цена за ОДНУ единицу товара при заказе от min_quantity штук",
    )
    min_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Минимальное количество, с которого действует эта цена за единицу",
    )
    currency: Mapped[str] = mapped_column(
        Enum(CurrencyCode),
        nullable=False,
        comment="Валюта (должна совпадать с валютой продукта)",
    )
