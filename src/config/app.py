import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

# from config.loguru_logger import configure_logger, logger
from config.logging_config import logger
from buyer.routers import router as buyer_router

from . import ROOT_DIR


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
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# include routers
# app.include_router(fub_router)

# routers registration
app.include_router(router=buyer_router, prefix='/chrome_extension/profiles/buyer',
                   tags=['Buyer'])


# register templates
templates_dir = os.path.join(ROOT_DIR, "templates")
templates = Jinja2Templates(directory=templates_dir)
