from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserSessionEntity:
    id: UUID | None
    user_id: int
    refresh_token: str
    current_jti: UUID
    exp: datetime
    revoked: bool = False
    revoked_at: datetime | None = None
    revoke_reason: str | None = None
