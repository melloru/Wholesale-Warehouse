from app.exceptions import AppError


class AuthenticationError(AppError):
    """Базовая ошибка аутентификации"""
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"


class AuthorizationError(AppError):
    """Ошибка авторизации"""
    status_code = 403
    error_code = "AUTHORIZATION_ERROR"


class PermissionDeniedError(AuthorizationError):
    """Доступ запрещен"""
    error_code = "PERMISSION_DENIED"
