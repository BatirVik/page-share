from fastapi import FastAPI
from loguru import logger

from app.logger import LoggerMiddleware
from app.config import config
from app.routes import router

app = FastAPI()
app.include_router(router)

logger.remove()
logger.add(config.LOGS_PATH, level="INFO", format="{time} {level} {message}")
app.add_middleware(LoggerMiddleware, logger=logger)
