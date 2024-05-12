import uvicorn
from fastapi import FastAPI, HTTPException
from loguru import logger

from logs.fastapi_events_logger import server_start_shutdown_logger
# from logs.legacy_logging_config import logger, server_start_shutdown_logger
from logs.logging_config import CustomLogger
from schemas.exceptions_schemas import (BadPayloadResponse, BadRequestResponse,
                                        ForbiddenResponse, NotAuthResponse,
                                        NotFoundResponse, ServerErrorResponse)

CustomLogger()

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
