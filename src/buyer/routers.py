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
def get_buyer_profile(
    access_level_key: str = Query(
        None, description="BASE64 of team_member@fb4s.com"),
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id")
):
    logger.info("*** API GET BUYER PROFILE TRIGGERED")
    return services.get_buyer_profile(access_level_key, profile_ekey, profile_ikey)


@router.get(
    "/leads",
    responses={
        200: {"model": schemas.BuyerLeads, "description": "Buyer Leads"}
    }
)
def get_buyer_leads(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id")
):
    logger.info("*** API GET BUYER LEADS LOCATIONS")
    return services.get_buyer_leads_service(profile_ekey=profile_ekey, profile_ikey=profile_ikey)


@router.get(
    "/evaluations",
    responses={
        200: {"model": schemas.BuyerInPersonEvaluations, "description": "Buyer In-Person Evaluations"}
    }
)
def get_buyer_in_person_evaluations(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id")
):
    logger.info("*** API GET BUYER In-Person EVALUATIONS")
    return services.get_buyer_in_person_evaluations_service(profile_ekey=profile_ekey, profile_ikey=profile_ikey)


@router.get(
    "/lead-score-events",
    responses={
        200: {"model": schemas.BuyerLeadScoreEvents, "description": "Buyer Lead Score Events"}
    }
)
def get_buyer_in_person_evaluations(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id")
):
    logger.info("*** API GET BUYER LEAD SCORE EVENTS")
    return services.get_buyer_lead_score_events(profile_ekey=profile_ekey, profile_ikey=profile_ikey)
