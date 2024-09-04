from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.logger import logger_middleware
from app import frontend, api

app = FastAPI()
app.include_router(api.router)
app.include_router(frontend.router)

STATIC_DIR_PATH = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR_PATH), name="static")

logger.remove(0)
app.middleware("http")(logger_middleware)
