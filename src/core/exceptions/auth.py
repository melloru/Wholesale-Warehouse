from core.exceptions.app import AppError


class AuthenticationError(AppError):
    """Базовая ошибка аутентификации"""
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"


class InvalidEmailOrPasswordError(AuthenticationError):
    error_code = "INVALID_EMAIL_OR_PASSWORD"

class AuthorizationError(AppError):
    """Ошибка авторизации"""
    status_code = 403
    error_code = "AUTHORIZATION_ERROR"


class PermissionDeniedError(AuthorizationError):
    """Доступ запрещен"""
    error_code = "PERMISSION_DENIED"

