from core.database.base_repository import SqlalchemyRepository
from auth.models import UserSession
from auth.schemas import SessionCreateDB


class SessionRepository(SqlalchemyRepository[UserSession, SessionCreateDB]):
    pass
