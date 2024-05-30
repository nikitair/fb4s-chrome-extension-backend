from fastapi import APIRouter
# from schemas import chrome_extension as schemas
from schemas.index import DefaultResponse


ce_router = APIRouter()


@ce_router.get("/", response_model = DefaultResponse)
async def chrome_extension_index():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "Chrome Extension",
    }
    

@ce_router.get("/buyer")
async def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None):
    return {
        "message": "Under Development"
    }
