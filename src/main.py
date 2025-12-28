import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import config
from core.database.db_helper import db_helper
from app.error_handlers import setup_system_error_handlers
from auth.routers.auth import router as auth_router
from users.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_system_error_handlers(app=app)
    yield
    await db_helper.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(auth_router)


def main():
    uvicorn.run(
        app="main:app",
        host=config.run.APP_HOST,
        port=config.run.APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
