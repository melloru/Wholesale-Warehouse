from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from core.constants import SessionFieldLengths


class SessionCreateRequest(BaseModel):
    user_id: int
    refresh_token: str
    expires_at: datetime


class SessionCreateDB(SessionCreateRequest):
    id: UUID
    revoked: bool | None = None
    revoked_at: datetime | None = None
    revoke_reason: str | None = Field(
        default=None,
        max_length=SessionFieldLengths.REVOKE_REASON,
    )


class SessionUpdateRequest(BaseModel):
    revoked: bool | None = None
    revoked_at: datetime | None = None
    revoke_reason: str | None = Field(
        default=None,
        max_length=SessionFieldLengths.REVOKE_REASON,
    )
