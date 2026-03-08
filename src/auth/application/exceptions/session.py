

class SessionError(Exception):
    """Ошибка сессии"""
    pass


class SessionNotFoundError(Exception):
    """Сессия не найдена"""
    pass


class SessionExpiredError(Exception):
    """Сессия истекла"""
    pass


class SessionRevokedError(Exception):
    """Сессия отозвана"""
    pass
