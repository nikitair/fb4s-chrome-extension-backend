import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from config.logging_config import logger, configure_logger
from config.middleware import log_middleware
from routers.fub import fub_router
from starlette.middleware.base import BaseHTTPMiddleware

# FastAPI Server Start / Shutdown lifespan manager
@asynccontextmanager
async def server_lifespan(app: FastAPI):
    """
    Logs FastAPI server Start and Shutdown events
    """

    # set timezone to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    # configure logger
    configure_logger()

    # log server start
    logger.warning(" == SERVER STARTED ==")
    yield
    # log server shutdown
    logger.warning("== SERVER STOPPED ==")


# app initialization
app = FastAPI(
    lifespan=server_lifespan
)

# middleware registration
app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=log_middleware)

# include routers
app.include_router(fub_router)


# routers registration
app.include_router(router=fub_router, prefix='/fub', tags=['fub'])


