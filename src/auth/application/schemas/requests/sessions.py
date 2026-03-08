from datetime import datetime

from pydantic import BaseModel, Field

from auth.application.domain.constants import SessionFieldLengths


class SessionUpdateRequest(BaseModel):
    revoked: bool | None = None
    revoked_at: datetime | None = None
    revoke_reason: str | None = Field(
        default=None,
        max_length=SessionFieldLengths.REVOKE_REASON,
    )
