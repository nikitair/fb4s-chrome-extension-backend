from config.logging_config import logger
from config.database import mysql



def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None):
    result = {
        "buyer_customer_id": None,
        "buyer_email": None,
        "buyer_phone_number": None,
        "buyer_first_name": None,
        "buyer_last_name": None,
        "viewer_is_admin": False
    }
    
    
    return result