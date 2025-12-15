from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions.db import DatabaseError


def setup_system_error_handlers(app: FastAPI):
    """
    Настройка обработчиков системных ошибок.
    Все эти ошибки возвращают 500 Internal Server Error.
    """

    @app.exception_handler(DatabaseError)
    async def database_error_handler(
        request: Request,
        exc: DatabaseError,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Database error",
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Unexpected error",
            },
        )
