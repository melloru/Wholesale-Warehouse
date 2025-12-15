import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.config import config
from auth.routers import router as users_router


app = FastAPI()
app.include_router(users_router)


@app.exception_handler(Exception)
def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


def main():
    uvicorn.run(
        app="main:app",
        host=config.run.APP_HOST,
        port=config.run.APP_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
