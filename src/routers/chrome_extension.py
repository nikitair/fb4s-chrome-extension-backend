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
    "/profiles/buyer",
    responses={
        200: {"model": schemas.BuyerProfileResponse, "description": "Buyer Profile"},
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


@ce_router.get(
    "/profiles/demo-buyer",
    responses={
        200: {"model": schemas.BuyerProfileResponse, "description": "Buyer Profile"},
        404: {"model": schemas.BuyerNotFoundResponse, "description": "Buyer NOT Found"}
    },
)
async def get_demo_buyer_profile(
    access_level_key: str = Query(None, description="BASE64 of team_member@fb4s.com"), 
    profile_ekey: str = Query(None, description="BASE64 of buyer@mail.com"), 
    profile_ikey: str = Query(None, description="BASE64 of buyer_customer_id")
):
    return {
        "id": 12345,
        "email": "john.johnson@mail.com",
        "phone_number": "123-123-1234",
        "first_name": "John",
        "last_name": "Johnson",
        "city": "Vancouver",
        "province": "British Columbia",
        "fub_stage": "A - Hot",
        "registration_time": "07:00 PM - 20 May 2024",
        "buyer_time_zone": "America/Vancouver",
        "buyer_local_time": "02:30 AM - 31 May 2024",
        "lead_score": 3.5,
        "assigned_realtor_name": "Dave Realtor",
        "assigned_realtor_email": "dave.realtor@fb4s.com",
        "profile_completed_levels": [
            "intro",
            "complete",
            "supplemental"
        ],
        "show_contacts": True
    }
