import uvicorn

from fastapi import FastAPI

from core.config import config
from app.error_handlers import setup_system_error_handlers
from auth.routers.auth import router as auth_router
from users.routers.users import router as users_router


app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)


def main():
    setup_system_error_handlers(app=app)
    uvicorn.run(
        app="main:app",
        host=config.run.APP_HOST,
        port=config.run.APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
