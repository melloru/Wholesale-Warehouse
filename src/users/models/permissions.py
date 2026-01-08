from sqlalchemy import UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base
from users.models.role_permission import RolePermission


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    code: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission"
    )

    __table_args__ = (UniqueConstraint("code", name="uq_permissions_code"),)
