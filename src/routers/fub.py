from fastapi import APIRouter

# from config.logging_config import logger
from schemas.default import DefaultResponse

fub_router = APIRouter()

@fub_router.get("/fub", response_model=DefaultResponse)
async def fub_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "fub",
    }
