from auth.models.sessions import Session
from auth.repositories.session_repository import SessionRepository
from auth.schemas.session_schemas import SessionCreateRequest
from core.services import BaseService


class SessionService(BaseService[SessionRepository, Session, SessionCreateRequest]):
    def __init__(self, repository: SessionRepository):
        super().__init__(repository)
