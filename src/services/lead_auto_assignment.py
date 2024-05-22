from config.database import mysql, mysql_queries
from config.logging_config import logger
from utils import lead_auto_assignment as utils


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

    formatted_payload = utils.na_formatter(payload)
    logger.info(f"LEAD TO ASSIGN - {formatted_payload}")

    postalcode: str = payload["postalcode"]
    listing_province: str = payload["listing_province"]
    listing_city: str = payload["listing_city"]
    listing_mls: str = payload["listing_mls"]
    listing_categories: str = payload["listing_categories"]
    buyer_name: str = payload["buyer_name"]
    buyer_email: str = payload["buyer_email"]
    buyer_city: str = payload["buyer_city"]
    buyer_province: str = payload["buyer_province"]
    cold_lead: str = payload["cold_lead"]

    # define values to process
    if cold_lead:
        province = buyer_province
        city = buyer_city
        postalcode = ""
    else:
        province = listing_province if listing_province else buyer_province
        city = listing_city if listing_city else buyer_city

    postalcode = utils.format_postalcode(postalcode)

    logger.debug(f"POLYGON SEARCH PARAMETERS: CITY - {city}; PROVINCE - {province}; POSTALCODE - {postalcode}")

    # evaluate buyer name
    sql_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=mysql_queries.get_buyer_firstname_by_email,
        params=[buyer_email]
    )

    return response
