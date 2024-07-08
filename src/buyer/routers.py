from fastapi import APIRouter, Query

from config.logging_config import logger
from buyer import schemas
from buyer import services
from buyer import utils

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
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET BUYER In-Person EVALUATIONS")
    return services.get_buyer_in_person_evaluations_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
    )


@router.get(
    "/lead-score-events",
    responses={
        200: {"model": schemas.BuyerLeadScoreEvents, "description": "Buyer Lead Score Events"}
    }
)
def get_buyer_in_person_evaluations(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET BUYER LEAD SCORE EVENTS")
    return services.get_buyer_lead_score_events_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
    )


@router.get(
    "/categories",
    responses={
        200: {"model": schemas.BuyerCategories, "description": "Buyer Categories"}
    }
)
def get_buyer_categories(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET BUYER CATEGORIES")
    return services.get_buyer_categories_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
    )


@router.get(
    "/viewed-listings",
    responses={
        200: {"model": schemas.BuyerViewedListings, "description": "Buyer Viewed Listings"}
    }
)
def get_buyer_viewed_listings(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET VIEWED LISTINGS")
    return services.get_buyer_viewed_listings_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
    )


@router.get(
    "/not-viewed-listings",
    responses={
        200: {"model": schemas.BuyerNotViewedListings, "description": "Buyer Not Viewed Listings"}
    }
)
def get_buyer_not_viewed_listings(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET NOT VIEWED LISTINGS")
    return services.get_buyer_not_viewed_listings_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
    )

@router.get(
    "/contact-seller-listings",
    responses={
        200: {"model": schemas.BuyerContactSellerListingListings, "description": "Buyer Contact Seller Listings"}
    }
)
def get_buyer_contact_seller_listings(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET CONTACT SELLER LISTINGS")
    return services.get_buyer_contact_seller_listings_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
    )


@router.get(
    "/all-green-buttons-listings",
    responses={
        200: {"model": schemas.BuyerGreenButtonListings, "description": "Buyer all Green Button clicks Listings"}
    }
)
def get_buyer_all_green_button_clicks_listings(
    profile_ekey: str = Query(None, description="PipeDrive: BASE64 of buyer@mail.com"),
    profile_ikey: str = Query(None, description="FUB: BASE64 of buyer_chat_id"),
    start_date: str = Query(utils.default_date_range()["start"], description="Search START Date (YYYY-MM-DD)"),
    end_date: str = Query(utils.default_date_range()["end"], description="Search START Date (YYYY-MM-DD)")
):
    logger.info("*** API GET ALL GREEN BUTTON CLICKS LISTINGS")
    return services.get_buyer_all_green_button_clicks_listings_service(
        profile_ekey=profile_ekey, 
        profile_ikey=profile_ikey,
        start_date=start_date,
        end_date=end_date
        )
