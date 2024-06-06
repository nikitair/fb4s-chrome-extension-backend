import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

# from config.loguru_logger import configure_logger, logger
from config.logging_config import logger
from config.middleware import log_middleware
from routers.chrome_extension import ce_router
from routers.fub import fub_router
from routers.lead_auto_assignment import las_router
from routers.textingduncan import td_router
from routers.tools import tools_router
from routers.eblast import eblast_router

from . import CORS_ORIGINS, ROOT_DIR


# FastAPI Server Start / Shutdown lifespan manager
@asynccontextmanager
async def server_lifespan(app: FastAPI):
    """
    FastAPI server Start and Shutdown events handler
    """

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
# app.add_middleware(middleware_class=BaseHTTPMiddleware,
#                    dispatch=log_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(fub_router)

# routers registration
app.include_router(router=ce_router, prefix='/chrome_extension',
                   tags=['Chrome Extension'])
app.include_router(router=tools_router, prefix='/eblast', tags=['E-Blast'])
app.include_router(router=fub_router, prefix='/fub', tags=['FUB'])
app.include_router(router=td_router, prefix='/textingduncan',
                   tags=['Texting Duncan'])
app.include_router(router=las_router, prefix='/las',
                   tags=['Lead Auto Assignment'])
app.include_router(router=tools_router, prefix='/tools', tags=['Tools'])


# register templates
templates_dir = os.path.join(ROOT_DIR, "templates")
templates = Jinja2Templates(directory=templates_dir)
