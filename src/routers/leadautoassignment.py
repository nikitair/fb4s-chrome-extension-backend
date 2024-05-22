from fastapi import APIRouter

from schemas.default import DefaultResponse

las_router = APIRouter()


@las_router.get("/las", response_model=DefaultResponse)
async def td_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "leadAutoAssignment",
    }
