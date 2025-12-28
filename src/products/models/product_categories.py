from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("product_categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    sort_order: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
        comment="Для порядка показа категорий",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_product_categories_name"),
        Index("idx_product_categories_parent_sort", "parent_id", "sort_order"),
    )
