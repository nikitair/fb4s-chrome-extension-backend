from fastapi import APIRouter

from config.logging_config import logger
from schemas.default import DefaultResponse
from schemas.lead_auto_assignment import LASRequest, LASResponse
from services.lead_auto_assignment import lead_auto_assignment

las_router = APIRouter()


@las_router.get("/", response_model=DefaultResponse)
async def las_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "leadAutoAssignment",
    }


@las_router.post("/assign_lead", response_model=LASResponse)
async def las_assign_lead_view(request: LASRequest):
    raw_payload: dict = request.dict()
    logger.debug(f"RAW PAYLOAD - {raw_payload}")

    result: dict = lead_auto_assignment(raw_payload)

    return result
