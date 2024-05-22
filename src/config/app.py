import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from config.loguru_logger import configure_logger, logger
from config.middleware import log_middleware
from routers.fub import fub_router
from routers.lead_auto_assignment import las_router
from routers.textingduncan import td_router


# FastAPI Server Start / Shutdown lifespan manager
@asynccontextmanager
async def server_lifespan(app: FastAPI):
    """
    FastAPI server Start and Shutdown events handler
    """
    configure_logger()

    # set timezone to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

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
app.include_router(router=td_router, prefix='/textingduncan', tags=['Texting Duncan'])
app.include_router(router=las_router, prefix='/las', tags=['Lead Auto Assignment'])
