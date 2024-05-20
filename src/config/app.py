import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from config.logging_config import logger, configure_logger
from config.middleware import log_middleware
from routers.fub import fub_router
from routers.textingduncan import td_router
from routers.leadautoassignment import las_router

from starlette.middleware.base import BaseHTTPMiddleware

# FastAPI Server Start / Shutdown lifespan manager
@asynccontextmanager
async def server_lifespan(app: FastAPI):
    """
    Logs FastAPI server Start and Shutdown events
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
app.include_router(router=td_router, prefix='/textingduncan', tags=['textingduncan'])
app.include_router(router=las_router, prefix='/leadAutoAssignment', tags=['leadAutoAssignment'])

