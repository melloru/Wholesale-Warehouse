from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from core.constants import SessionFieldLengths


class SessionCreateRequest(BaseModel):
    user_id: int


class SessionCreateDB(SessionCreateRequest):
    id: UUID
    refresh_token: str
    current_jti: UUID
    revoked: bool | None = None
    revoked_at: datetime | None = None
    revoke_reason: str | None = Field(
        default=None,
        max_length=SessionFieldLengths.REVOKE_REASON,
    )
    expires_at: datetime


class SessionUpdateRequest(BaseModel):
    revoked: bool | None = None
    revoked_at: datetime | None = None
    revoke_reason: str | None = Field(
        default=None,
        max_length=SessionFieldLengths.REVOKE_REASON,
    )
