import uvicorn
from fastapi import FastAPI

from src.core.config import config


app = FastAPI()


def main():
    uvicorn.run(
        app="main:app",
        host=config.run.APP_HOST,
        port=config.run.APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
