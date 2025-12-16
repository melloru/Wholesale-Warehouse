from app.exceptions import AppError


class DatabaseError(AppError):
    """Базовое исключение БД"""

    status_code = 500
    error_code = "DATABASE_ERROR"

    def __init__(self, message: str = "Database error", **kwargs):
        super().__init__(message, **kwargs)
