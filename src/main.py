import uvicorn
from fastapi import FastAPI

from config.app import server_start_shutdown_logger
from config.logging_config import logger
from routers.fub import fub_router

app = FastAPI(lifespan=server_start_shutdown_logger)
app.include_router(router=fub_router, prefix='/fub', tags=['fub'])


@app.get('/')
async def index_view():
    logger.info(f"{index_view.__name__} -- INDEX VIEW TRIGGERED")
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "root"
    }

if __name__ == "__main__":
    # dev server run
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
