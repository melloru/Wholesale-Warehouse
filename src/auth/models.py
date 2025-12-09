import uuid

from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    UniqueConstraint,
    Index,
    String,
    ForeignKey,
    UUID,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableDict

from core.models import Base
from core.mixins import TimestampMixin
from core.constants import FieldLengths
from auth.enums import UserRole, UserStatus


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(FieldLengths.EMAIL), nullable=False)
    password_hash: Mapped[str] = mapped_column(
        String(FieldLengths.PASSWORD_HASH),
        nullable=False,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(FieldLengths.NAME),
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(FieldLengths.NAME),
        nullable=True,
    )
    public_name: Mapped[str | None] = mapped_column(
        String(FieldLengths.PUBLIC_NAME),
        nullable=True,
    )

    phone_number: Mapped[int | None] = mapped_column(
        String(FieldLengths.PHONE),
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


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    refresh_token: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    revoke_reason: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    __table_args__ = (
        Index("ix_sessions_user_id", "user_id", "revoked"),
        Index("ix_sessions_expires_at_revoked", "expires_at", "revoked"),
        Index("ix_sessions_user_id_expires_at", "user_id", "expires_at"),
        Index("ix_sessions_created_at", "created_at"),
    )
