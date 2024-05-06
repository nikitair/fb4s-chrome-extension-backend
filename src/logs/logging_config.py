import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

ROOT_DIR = os.getcwd()


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, timezone.utc)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ' UTC'


# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Custom UTC formatter
formatter = UTCFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Terminal output
th = logging.StreamHandler()
th.setLevel(logging.INFO)
th.setFormatter(formatter)
logger.addHandler(th)

# File output
fh = logging.FileHandler(f"{ROOT_DIR}/logs/logs{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')}.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)


# FastAPI Server Start / Shutdown logging lifespan manager
@asynccontextmanager
async def serer_start_shutdown_logger(app: FastAPI):
    """
    Logs FastAPI server Start and Shutdown events
    """
    logger.warning(" == SERVER STARTED ==")
    yield
    logger.warning("== SERVER STOPPED ==")
