from auth.exceptions.auth import AuthenticationError


class SessionError(AuthenticationError):
    """Ошибка сессии"""
    error_code = "SESSION_ERROR"


class SessionNotFoundError(SessionError):
    """Сессия не найдена"""
    error_code = "SESSION_NOT_FOUND"


class SessionExpiredError(SessionError):
    """Сессия истекла"""
    error_code = "SESSION_EXPIRED"


class SessionRevokedError(SessionError):
    """Сессия отозвана"""
    error_code = "SESSION_REVOKED"
