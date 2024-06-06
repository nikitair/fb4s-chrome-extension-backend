from config.logging_config import logger
from utils import chrome_extension as utils
from schemas import chrome_extension as schemas


def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None) -> dict:
    logger.info(f"GET BUYER PROFILE")
    buyer_profile = {
        "id": None,
        "email": None,
        "phone_number": None,
        "first_name": None,
        "last_name": None,
        "city": None,
        "province": None,
        "fub_stage": "Not a FUB Buyer",
        "registration_time": None,
        "buyer_time_zone": None,
        "lead_score": None,
        "assigned_realtor_name": None,
        "assigned_realtor_email": None,
        "profile_completed_levels": {
            "intro": False,
            "complete": False,
            "supplemental": False
        },
        "show_contacts": False,
        "sign_rca_form_url": "https://www.findbusinesses4sale.com/"
    }
    
    viewer_email = utils.decode_base64_item(access_level_key)
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"access_level_key = {access_level_key} -> {viewer_email}")
    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email, buyer_chat_id)
    logger.info(f"BUYER DATA - {buyer_data}")
    
    if buyer_data:
        buyer_profile.update(buyer_data)
        buyer_email = buyer_data["email"]
    
        # checking viewer permission
        viewer_is_admin = utils.check_if_viewer_is_admin(viewer_email)
        rca_signed = utils.sql_m_check_if_rca_signed(viewer_email, buyer_email)
        if viewer_is_admin:
            buyer_profile["show_contacts"] = True
        else:
            buyer_profile["show_contacts"] = rca_signed
            logger.info(f"RCA SIGNED - {rca_signed}")
            
        # evaluating buyer lead score
        lead_score = utils.sql_p_get_buyer_lead_score(buyer_email)
        buyer_profile["lead_score"] = lead_score
        logger.info(f"BUYER LEAD SCORE - {lead_score}")
        
        # get fub stage
        buyer_fub_stage = utils.get_buyer_fub_stage(buyer_email)
        buyer_profile["fub_stage"] = buyer_fub_stage
        logger.info(f"BUYER FUB STAGE - {buyer_fub_stage}")
        
        # get assigned realtor
        assigned_reator_data = utils.sql_m_get_buyer_assigned_realtor(buyer_email)
        logger.info(f"ASSIGNED REATOR - {assigned_reator_data}")
        if assigned_reator_data:
            buyer_profile["assigned_realtor_email"] = assigned_reator_data["assigned_realtor_email"]
            buyer_profile["assigned_realtor_name"] = assigned_reator_data["assigned_realtor_name"]
            
        # get buyer UTC offset
        buyer_city = buyer_profile["city"]
        if not buyer_city:
            buyer_predefigned_location = utils.sql_p_get_predefigned_location(buyer_profile["id"])
            logger.info(f"BUYER PREDEFIGNED LOCATION - {buyer_predefigned_location}")
            if buyer_predefigned_location:
                buyer_city = buyer_predefigned_location["city"]
                
        timezone = utils.get_timezone(buyer_city)  
        utc_offset = utils.get_utc_offset(timezone)
        buyer_profile["buyer_time_zone"] = utc_offset
        logger.info(f"BUYER TIME ZONE - {timezone}; UTC OFFSET - {utc_offset}")
        
        # get profile completed levels
        profile_completed_levels = utils.sql_m_get_profile_completed_levels(buyer_email)
        if profile_completed_levels:
            buyer_profile["profile_completed_levels"] = profile_completed_levels
            logger.info(f"PROFILE COMPLETED LEVELS - {profile_completed_levels}")
            
        # RCA link
        if not rca_signed:
            buyer_id = buyer_profile["id"]
            sign_rca_link = utils.prepare_sign_rca_link(buyer_id)
            logger.info(f"SIGN RCA LINK - {sign_rca_link}")
            buyer_profile["sign_rca_form_url"] = sign_rca_link
            
    logger.info(f"BUYER PROFILE RESPONSE - {buyer_profile}")
    return buyer_profile
