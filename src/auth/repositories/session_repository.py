from core.repositories import SqlalchemyRepository
from auth.models.sessions import Session
from auth.schemas.session_schemas import SessionCreateDB


class SessionRepository(SqlalchemyRepository[Session, SessionCreateDB]):
    pass


def get_session_repository() -> SessionRepository:
    return SessionRepository(Session)
