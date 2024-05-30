from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from schemas import chrome_extension as schemas
from schemas.index import DefaultResponse
from services import chrome_extension as services


ce_router = APIRouter()


@ce_router.get("/", response_model = DefaultResponse)
async def chrome_extension_index():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "Chrome Extension",
    }
    

@ce_router.get("/buyer", response_model=schemas.GetBuyerProfileResponse)
async def get_buyer_profile(
    access_level_key: str = Query(None, description="base64(team_member@fb4s.com)"), 
    profile_ekey: str = Query(None, description="base64(buyer@mail.com)"), 
    profile_ikey: str = Query(None, description="base64(buyer_customer_id)")
    ):
    result = services.get_buyer_profile(access_level_key, profile_ekey, profile_ikey)
    
    if not result:
        raise HTTPException(status_code=404, detail="Buyer NOT found")
        
    return result
