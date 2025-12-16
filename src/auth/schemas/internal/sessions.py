from uuid import UUID

from auth.schemas.requests.sessions import SessionCreateRequest


class SessionCreateDB(SessionCreateRequest):
    id: UUID
