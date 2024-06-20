from fastapi import APIRouter, Query

from config.logging_config import logger
from buyer import schemas
from buyer import services

router = APIRouter()


@router.get(
    "/",
    responses={
        200: {"model": schemas.BuyerProfileResponse, "description": "Buyer Profile"}
    },
)
async def get_buyer_profile(
    access_level_key: str = Query(
        None, description="BASE64 of team_member@fb4s.com"),
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id")
):
    logger.info("*** GET BUYER PROFILE TRIGGERED")
    return services.get_buyer_profile(access_level_key, profile_ekey, profile_ikey)
