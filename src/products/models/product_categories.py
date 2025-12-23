from sqlalchemy import (
    String,
    Text,
    ForeignKey,
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
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
