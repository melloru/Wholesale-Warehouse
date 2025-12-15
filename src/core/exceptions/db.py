from core.exceptions.app import AppError


class DatabaseError(AppError):
    status_code = 500
    error_code = "DATABASE_ERROR"

    def __init__(self, message: str = "Database error", **kwargs):
        super().__init__(message, **kwargs)


class DatabaseConnectionError(DatabaseError):
    """Ошибка подключения к БД"""

    error_code = "DATABASE_CONNECTION_ERROR"


class DatabaseQueryError(DatabaseError):
    """Ошибка выполнения запроса"""

    error_code = "DATABASE_QUERY_ERROR"


class DatabaseConstraintError(DatabaseError):
    """Нарушение ограничений БД"""

    status_code = 400
    error_code = "DATABASE_CONSTRAINT_ERROR"
