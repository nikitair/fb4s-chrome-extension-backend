from fastapi import APIRouter

from config.logging_config import logger
from schemas.default import DefaultResponse

fub_router = APIRouter()

@fub_router.get("/", response_model=DefaultResponse)
def fub_index_view():
    logger.info(f"{fub_index_view.__name__} -- FUB INDEX VIEW TRIGGERED")
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "fub",
    }
