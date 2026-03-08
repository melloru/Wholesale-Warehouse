from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Text, BigInteger, DateTime
from sqlalchemy.sql.functions import func

from core.infrastructure.database.models import Base


class UserBlockPermissions(Base):
    __tablename__ = "user_block_permissions"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
    )
    blocked_by_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
    )
    reason: Mapped[str] = mapped_column(Text)
    blocked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
