import uuid

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Index,
    String,
    ForeignKey,
    UUID,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.mixins import TimestampMixin
from core.constants import SessionFieldLengths


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
        String(SessionFieldLengths.REVOKE_REASON),
        nullable=True,
    )

    __table_args__ = (
        Index("ix_sessions_user_id", "user_id", "revoked"),
        Index("ix_sessions_expires_at_revoked", "expires_at", "revoked"),
        Index("ix_sessions_user_id_expires_at", "user_id", "expires_at"),
        Index("ix_sessions_created_at", "created_at"),
    )
