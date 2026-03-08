class AppError(Exception):
    """Базовое исключение приложения"""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        status_code: int = 500,
        details: dict | None = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.status_code = status_code
        self.details = details or {}
