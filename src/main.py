import uvicorn

from fastapi import FastAPI

from core.config import config
from auth.routers import router as users_router


app = FastAPI()
app.include_router(users_router)


def main():
    uvicorn.run(
        app="main:app",
        host=config.run.APP_HOST,
        port=config.run.APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
