import uvicorn
from config.logging_config import logger

from config.app import app


@app.get('/')
async def index_view():
    logger.debug(f"{index_view.__name__} -- INDEX VIEW TRIGGERED")
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "root"
    }

if __name__ == "__main__":
    # dev server run
    # module : app
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
