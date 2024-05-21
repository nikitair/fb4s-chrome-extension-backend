from fastapi import APIRouter
from schemas.default import DefaultResponse

td_router = APIRouter()


@td_router.get("/fub", response_model=DefaultResponse)
async def td_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "textingduncan",
    }
