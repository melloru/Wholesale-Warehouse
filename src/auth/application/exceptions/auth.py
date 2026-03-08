from core.exceptions import AppError


class AuthenticationError(AppError):
    """Базовая ошибка аутентификации"""
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"

class PermissionDeniedError(AppError):
    """Доступ запрещен"""
    error_code = "PERMISSION_DENIED"
