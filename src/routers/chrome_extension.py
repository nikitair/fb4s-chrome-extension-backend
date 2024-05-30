from fastapi import APIRouter
from schemas import chrome_extension as schemas
from schemas.index import DefaultResponse


ce_router = APIRouter()


@ce_router.get("/", response_model = DefaultResponse)
async def chrome_extension_index():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "Chrome Extension",
    }
    
