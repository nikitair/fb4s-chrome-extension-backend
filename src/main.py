import uvicorn
from fastapi import FastAPI
from logs.logging_config import logger

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.warning(" == SERVER STARTED ==")


@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("== SERVER STOPPED ==")


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
