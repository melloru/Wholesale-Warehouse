from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from sqlalchemy.sql.schema import Index, UniqueConstraint, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Enum, String, BigInteger, ARRAY


from core.infrastructure.database.models import Base
from core.infrastructure.database.mixins import TimestampMixin
from core.config.permissions import RoleEnum
from users.domain.constants import UserFieldLengths
from users.domain.entities import UserEntity
from users.domain.enums import UserStatus

if TYPE_CHECKING:
    from users.infrastructure.database.models import Role


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        default=RoleEnum.USER.id,
        server_default=text("1"),
    )

    email: Mapped[str] = mapped_column(
        String(UserFieldLengths.EMAIL),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(UserFieldLengths.PASSWORD_HASH),
        nullable=False,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(UserFieldLengths.NAME),
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(UserFieldLengths.NAME),
        nullable=True,
    )
    public_name: Mapped[str | None] = mapped_column(
        String(UserFieldLengths.PUBLIC_NAME),
        nullable=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(UserFieldLengths.PHONE),
        nullable=True,
    )
    phone_verified: Mapped[bool] = mapped_column(default=False)
    email_verified: Mapped[bool] = mapped_column(default=False)

    blocked_permissions: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"),
        default=UserStatus.PENDING,
        nullable=False,
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )

    role: Mapped["Role"] = relationship(back_populates="users")

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("idx_users_status", "status"),
        Index("idx_users_role_status", "role_id", "status"),
    )
