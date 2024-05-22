from fastapi import APIRouter

from schemas.index import DefaultResponse

fub_router = APIRouter()


@fub_router.get("/", response_model=DefaultResponse)
async def fub_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "fub",
    }
