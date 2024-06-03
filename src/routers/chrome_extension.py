from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from config.logging_config import logger
from schemas import chrome_extension as schemas
from schemas.index import DefaultResponse
from services import chrome_extension as services
from typing import Union

ce_router = APIRouter()


@ce_router.get("/", response_model=DefaultResponse)
async def chrome_extension_index():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "Chrome Extension",
    }


@ce_router.get(
    "/profiles/buyer",
    responses={
        200: {"model": schemas.BuyerProfileResponse, "description": "Buyer Profile"}
    },
)
async def get_buyer_profile(
    access_level_key: str = Query(
        None, description="BASE64 of team_member@fb4s.com"),
    profile_ekey: str = Query(None, description="BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="BASE64 of buyer_customer_id")
):
    return services.get_buyer_profile(access_level_key, profile_ekey, profile_ikey)


@ce_router.get(
    "/profiles/demo-buyer",
    responses={
        200: {"model": schemas.BuyerProfileResponse, "description": "Buyer Profile"}
    },
)
async def get_demo_buyer_profile(
    access_level_key: str = Query(
        None, description="BASE64 of team_member@fb4s.com"),
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
        "buyer_time_zone": -10,
        "lead_score": 3.5,
        "assigned_realtor_name": "Dave Realtor",
        "assigned_realtor_email": "dave.realtor@fb4s.com",
        "profile_completed_levels": {
            "intro": True,
            "complete": True,
            "supplemental": False
        },
        "show_contacts": True
    }
