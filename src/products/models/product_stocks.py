from sqlalchemy import Index, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base
from core.database.mixins import TimestampMixin


class ProductStock(Base, TimestampMixin):
    __tablename__ = "product_stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    available_quantity: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    reserved_quantity: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
        comment="Зарезервировано в активных заказах",
    )
    is_on_demand: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Товар поставляется под заказ (нет на складе)",
    )

    __table_args__ = (
        UniqueConstraint("product_id", name="uq_product_stocks_product_id"),
        Index(
            "idx_product_stocks_product_id_available_qty",
            "product_id",
            "available_quantity",
        ),
    )
