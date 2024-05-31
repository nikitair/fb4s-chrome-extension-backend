from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from config.logging_config import logger
from schemas import chrome_extension as schemas
from schemas.index import DefaultResponse
from services import chrome_extension as services
from typing import Union

ce_router = APIRouter()


@ce_router.get("/", response_model = DefaultResponse)
async def chrome_extension_index():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "Chrome Extension",
    }
    

@ce_router.get(
    "/buyer",
    responses={
        200: {"model": schemas.GetBuyerProfileResponse, "description": "Buyer Profile"},
        404: {"model": schemas.BuyerNotFoundResponse, "description": "Buyer NOT Found"}
    },
)
async def get_buyer_profile(
    access_level_key: str = Query(None, description="BASE64 of team_member@fb4s.com"), 
    profile_ekey: str = Query(None, description="BASE64 of buyer@mail.com"), 
    profile_ikey: str = Query(None, description="BASE64 of buyer_customer_id")
):
    logger.debug(f"access_level_key: {access_level_key}")
    logger.debug(f"profile_ekey: {profile_ekey}")
    logger.debug(f"profile_ikey: {profile_ikey}")

    result = services.get_buyer_profile(access_level_key, profile_ekey, profile_ikey)
    if not result:
        logger.error("Buyer not found")
        return JSONResponse(
            content={"error": "Buyer NOT found"}, status_code=404
        )
    
    logger.info(f"RESPONSE - {result}")
    return result
