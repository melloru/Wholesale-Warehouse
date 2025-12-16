from core.database.repositories import SqlalchemyRepository
from auth.models import UserSession
from auth.schemas import SessionCreateDB


class SessionRepository(SqlalchemyRepository[UserSession, SessionCreateDB]):
    pass


def get_session_repository() -> SessionRepository:
    return SessionRepository(UserSession)
