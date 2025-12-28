from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Integer,
    Index,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base
from core.database.mixins import TimestampMixin


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
        comment="Цена (в центах) за ОДНУ единицу товара при заказе от min_quantity штук",
    )
    min_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Минимальное количество, с которого действует эта цена за единицу",
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "min_quantity",
            name="uq_product_prices_product_id_min_qty",
        ),
        Index(
            "idx_product_prices_product_id_min_qty_for_quantity",
            "product_id",
            text("min_quantity DESC"),
        ),
        Index(
            "idx_product_prices_quantity_price",
            "min_quantity",
            "price_per_unit_minor",
        ),
        Index(
            "idx_product_prices_price_quantity",
            "price_per_unit_minor",
            "min_quantity",
        ),
    )
