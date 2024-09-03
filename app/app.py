from fastapi import FastAPI
from loguru import logger

from app.logger import LoggerMiddleware
from app.config import config
from app import frontend, api

app = FastAPI()
app.include_router(api.router)
app.include_router(frontend.router)

logger.remove()
logger.add(config.LOGS_PATH, level="INFO", format="{time} {level} {message}")
app.add_middleware(LoggerMiddleware, logger=logger)
