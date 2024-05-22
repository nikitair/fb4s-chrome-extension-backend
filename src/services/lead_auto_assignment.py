from utils.lead_auto_assignment import na_formatter
from config.logging_config import logger


def lead_auto_assignment(payload: dict):
    response = {
        "assigned_realtor": "willow@fb4s.com",
        "possible_realtors": [
        ],
        "realtor_type_1": 1,
        "assigned_pond_id": 0,
        "detailed_info": {
            "win_type": "pond",
            "realtor_category": None,
            "buyer_nationality": None,
            "realtor_priority": None
        }
    }

    formatted_payload = na_formatter(payload)
    logger.info(f"LEAD TO ASSIGN - {formatted_payload}")

    postalcode: str = payload["postalcode"]
    listing_province: str = payload["listing_province"]
    listing_city: str = payload["listing_city"]
    listing_mls: str = payload["listing_mls"]
    listing_categories: str = payload["listing_categories"]
    buyer_name: str = payload["buyer_name"]
    buyer_email: str = payload["buyer_email"]
    cold_lead: str = payload["cold_lead"]

    return response
