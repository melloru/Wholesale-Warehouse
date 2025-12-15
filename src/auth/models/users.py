from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    UniqueConstraint,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableDict

from core.database.models import Base
from core.database.mixins import TimestampMixin
from core.constants import UserFieldLengths
from auth.enums import UserRole, UserStatus


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

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

    phone_number: Mapped[int | None] = mapped_column(
        String(UserFieldLengths.PHONE),
        nullable=True,
    )
    phone_verified: Mapped[bool] = mapped_column(default=False)
    email_verified: Mapped[bool] = mapped_column(default=False)

    permissions: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSON),
        default=dict,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.CUSTOMER,
        nullable=False,
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"),
        default=UserStatus.PENDING,
        nullable=False,
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_superadmin: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)

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

    __table_args__ = (
        UniqueConstraint("email", name="ux_users_email"),
        Index("ix_users_email", "email"),
        Index("ix_users_status", "status"),
        Index("ix_users_role_status", "role", "status"),
    )
