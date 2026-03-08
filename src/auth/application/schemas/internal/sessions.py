from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from auth.application.domain.constants import SessionFieldLengths


class SessionCreateInternal(BaseModel):
    id: UUID
    user_id: int
    refresh_token: str
    current_jti: UUID
    revoked: bool | None = None
    revoked_at: datetime | None = None
    revoke_reason: str | None = Field(
        default=None,
        max_length=SessionFieldLengths.REVOKE_REASON,
    )
    exp: datetime
