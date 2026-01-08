from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base

if TYPE_CHECKING:
    from users.models import Role
    from users.models import Permission


class RolePermission(Base):
    __tablename__ = "role_permission"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey(column="roles.id", ondelete="CASCADE")
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey(column="permissions.id", ondelete="CASCADE")
    )

    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
