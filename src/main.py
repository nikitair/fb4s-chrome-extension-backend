import uvicorn

from config.app import app
# from config.loguru_logger import logger
from config.logging_config import logger


@app.get('/', tags=['index'])
async def index_view():
    logger.debug(f"{index_view.__name__} -- INDEX VIEW TRIGGERED")
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "root"
    }


if __name__ == "__main__":
    # module : app
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    # uvicorn.run("main:app", host="0.0.0.0", port=5003, reload=True)
