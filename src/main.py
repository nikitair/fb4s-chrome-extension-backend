import uvicorn
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from logs.logging_config import logger
# from logs.legacy_logging_config import logger, server_start_shutdown_logger
from schemas.exceptions_schemas import (BadPayloadResponse, BadRequestResponse,
                                        ForbiddenResponse, NotAuthResponse,
                                        NotFoundResponse, ServerErrorResponse)


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


# TODO:
# - override HTTPS exceptions
# - rewrite unit tests according to it
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):

    match exc.status_code:
        case 404:
            return NotFoundResponse
        case 400:
            return BadRequestResponse
        case 401:
            return NotAuthResponse
        case 403:
            return ForbiddenResponse
        case 415:
            return BadPayloadResponse
        case 500:
            return ServerErrorResponse

        case _:
            return await request.app.handle_exception(request, exc)

# -------------------------------- VIEWS ---------------------------------------------------------------------------------------------------------


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
