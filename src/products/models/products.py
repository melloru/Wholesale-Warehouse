from sqlalchemy import (
    Enum,
    String,
    BigInteger,
    Text,
    ForeignKey,
    Float,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base
from core.database.mixins import TimestampMixin
from products.constants import ProductsFieldLength
from products.enums import ProductStatus, CurrencyCode


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(ProductsFieldLength.NAME),
        nullable=False,
    )
    price_per_unit_minor: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Цена за ОДНУ единицу товара",
    )
    currency: Mapped[str] = mapped_column(
        Enum(CurrencyCode, name="product_currency"),
        default=CurrencyCode.USD,
        nullable=False,
    )
    min_order_quantity: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    weight_kg: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        Enum(ProductStatus, name="product_status"),
        default=ProductStatus.PENDING,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_products_name"),
        Index("idx_products_category_id", "category_id"),
        Index("idx_products_status", "status"),
        Index(
            "idx_products_category_id_status",
            "category_id",
            "status",
        ),
    )
