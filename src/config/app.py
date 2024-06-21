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

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# routers registration
app.include_router(router=buyer_router, prefix='/chrome_extension/profiles/buyer',
                   tags=['Buyer'])


# register templates
templates_dir = os.path.join(ROOT_DIR, "templates")
templates = Jinja2Templates(directory=templates_dir)
