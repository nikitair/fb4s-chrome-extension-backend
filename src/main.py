from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.logging_config import logger


# FastAPI Server Start / Shutdown logging lifespan manager
@asynccontextmanager
async def server_start_shutdown_logger(app: FastAPI):
    """
    Logs FastAPI server Start and Shutdown events
    """
    logger.warning(" == SERVER STARTED ==")
    yield
    logger.warning("== SERVER STOPPED ==")


app = FastAPI(lifespan=server_start_shutdown_logger)


@app.get('/')
async def index_view():
    logger.info(f"{index_view.__name__} -- INDEX VIEW TRIGGERED")
    return {
        "service": "FB4S Automations",
        "success": True
    }

if __name__ == "__main__":
    # dev server run
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
