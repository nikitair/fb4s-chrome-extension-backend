from contextlib import asynccontextmanager

from fastapi import FastAPI
from logging_config import CustomLogger
from loguru import logger

CustomLogger()


# FastAPI Server Start / Shutdown logging lifespan manager
@asynccontextmanager
async def server_start_shutdown_logger(app: FastAPI):
    """
    Logs FastAPI server Start and Shutdown events
    """
    logger.warning(" == SERVER STARTED ==")
    yield
    logger.warning("== SERVER STOPPED ==")
