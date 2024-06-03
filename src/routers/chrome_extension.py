from typing import Union

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from config.logging_config import logger
from schemas import chrome_extension as schemas
from schemas.index import DefaultResponse
from services import chrome_extension as services

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
    logger.info("*** GET BUYER PROFILE TRIGGERED")
    return services.get_buyer_profile(access_level_key, profile_ekey, profile_ikey)
