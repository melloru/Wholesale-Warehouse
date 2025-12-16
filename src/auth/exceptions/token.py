from auth.exceptions.auth import AuthenticationError


class TokenError(AuthenticationError):
    """Ошибка токена"""
    error_code = "TOKEN_ERROR"


class TokenInvalidError(TokenError):
    """Невалидный токен"""
    error_code = "TOKEN_INVALID"


class TokenExpiredError(TokenError):
    """Токен истек"""
    error_code = "TOKEN_EXPIRED"


class TokenMismatchError(TokenError):
    """Несоответствие токена"""
    error_code = "TOKEN_MISMATCH"
