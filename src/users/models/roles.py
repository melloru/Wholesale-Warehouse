from sqlalchemy import Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base
from users.models.role_permission import RolePermission


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="role"
    )

    __table_args__ = (UniqueConstraint("name", name="uq_roles_name"),)
