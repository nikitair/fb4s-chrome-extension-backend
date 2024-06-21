from config.logging_config import logger
from buyer import utils


def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None) -> dict:
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


def get_buyer_leads_service(profile_ekey: str = None, profile_ikey: str = None) -> list:
    leads = []
    
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email=buyer_email, buyer_chat_id=buyer_chat_id)
    if buyer_data:
        logger.info(f"BUYER DATA - ({buyer_data})")
        buyer_id = buyer_data["id"]

        # get buyer leads
        leads = utils.sql_m_get_buyer_leads(buyer_id=buyer_id)
    
    logger.info(f"LEADS FOUND - ({leads})")
    return {"leads": leads}


def get_buyer_in_person_evaluations_service(profile_ekey: str = None, profile_ikey: str = None) -> list:
    evaluations = []
    
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email=buyer_email, buyer_chat_id=buyer_chat_id)
    if buyer_data:
        logger.info(f"BUYER DATA - ({buyer_data})")
        buyer_email = buyer_data["email"]

        # get buyer in-person evaluations
        evaluations = utils.sql_p_get_in_person_evaluation(buyer_email=buyer_email)
    
    logger.info(f"In-Person EVALUATION FOUND - ({evaluations})")
    return {"evaluations": evaluations}


def get_buyer_lead_score_events_service(profile_ekey: str = None, profile_ikey: str = None) -> list:
    events = []
    
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email=buyer_email, buyer_chat_id=buyer_chat_id)
    if buyer_data:
        logger.info(f"BUYER DATA - ({buyer_data})")
        buyer_email = buyer_data["email"]

        # get buyer lead score events
        events = utils.sql_p_get_leads_score_events(buyer_email=buyer_email)
    
    logger.info(f"LEAD SCORE EVENTS FOUND - ({events})")
    return {"events": events}


def get_buyer_categories_service(profile_ekey: str = None, profile_ikey: str = None) -> list:
    categories = []
    
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email=buyer_email, buyer_chat_id=buyer_chat_id)
    if buyer_data:
        logger.info(f"BUYER DATA - ({buyer_data})")
        buyer_email = buyer_data["email"]
        
        buyer_mls_list = []
        
        # get viewed listings
        viewed_listings_data = utils.sql_p_get_view_listing_events(buyer_email=buyer_email)
        if viewed_listings_data:
            viewed_listings = [item["mls"] for item in viewed_listings_data]
            logger.info(f"VIEWED LISTINGS - ({viewed_listings})")
            buyer_mls_list.extend(viewed_listings)
            
        # get contact seller listings
        contact_seller_listings_data = utils.sql_p_get_contacted_seller_events(buyer_email)
        if contact_seller_listings_data:
            contact_seller_listings = [item["mls"] for item in contact_seller_listings_data]
            logger.info(f"CONTACT SELLER LISTINGS - ({contact_seller_listings})")
            buyer_mls_list.extend(contact_seller_listings)
            
        # get all green button listings
        all_green_button_listings_data = utils.sql_p_get_all_green_button_click_events(buyer_email)
        if all_green_button_listings_data:
            all_green_button_listings = [item["mls"] for item in all_green_button_listings_data]
            logger.info(f"ALL GREEN BUTTON LISTINGS - ({all_green_button_listings})")
            buyer_mls_list.extend(all_green_button_listings)
            
        buyer_mls_list = list(set(buyer_mls_list))
        logger.info(f"BUYER MLS LIST - ({buyer_mls_list})")
        
        if buyer_mls_list:
            categories = utils.sql_m_get_buyer_categories(buyer_mls_list)
            
    logger.info(f"BUYER CATEGORIES FOUND - ({categories})")
    return {"categories": categories}


def get_buyer_viewed_listings_service(profile_ekey: str = None, profile_ikey: str = None) -> list:
    listings = []
    
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email=buyer_email, buyer_chat_id=buyer_chat_id)
    if buyer_data:
        logger.info(f"BUYER DATA - ({buyer_data})")
        buyer_email = buyer_data["email"]
        
        mls_list = []
        
        # get viewed listings
        viewed_listings_data = utils.sql_p_get_view_listing_events(buyer_email=buyer_email)
        if viewed_listings_data:
            viewed_listings = [item["mls"] for item in viewed_listings_data]
            logger.info(f"VIEWED LISTINGS - ({viewed_listings})")
            mls_list.extend(viewed_listings)
        
        if mls_list:
            listings_details= utils.sql_m_get_mls_data(mls_list)
            logger.info(f"LISTINGS DETAILS - ({listings_details})")
            
            if listings_details:
                
                for listing in viewed_listings_data:
                    mls = listing["mls"]
                    
                    listing.update(
                        listings_details[mls]
                    )
                    
                listings = viewed_listings_data
            
    logger.info(f"BUYER VIEWED LISTINGS FOUND - ({listings})")
    return {"listings": listings}



def get_buyer_not_viewed_listings_service(profile_ekey: str = None, profile_ikey: str = None) -> list:
    listings = []
    
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_chat_id = utils.decode_base64_item(profile_ikey)

    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_chat_id}")
    
    # get buyer data
    buyer_data = utils.sql_m_get_buyer(buyer_email=buyer_email, buyer_chat_id=buyer_chat_id)
    if buyer_data:
        logger.info(f"BUYER DATA - ({buyer_data})")
        buyer_email = buyer_data["email"]
        
        buyer_mls_list = []
        buyer_province_list = []
        buyer_category_list = []
        
        # get viewed listings
        viewed_listings_data = utils.sql_p_get_view_listing_events(buyer_email=buyer_email)
        if viewed_listings_data:
            viewed_listings = [item["mls"] for item in viewed_listings_data]
            logger.info(f"VIEWED LISTINGS - ({viewed_listings})")
            buyer_mls_list.extend(viewed_listings)
            
            viewed_listings_details: dict = utils.sql_m_get_mls_data(viewed_listings)
            logger.info(f"VIEWED LISTINGS DETAILS - ({viewed_listings_details})")
            
            if viewed_listings_details:
                for listing in viewed_listings_data:
                    mls = listing["mls"]
                    listing.update(viewed_listings_details[mls])

                viewed_provinces = [item["province"] for item in viewed_listings_data]
                logger.info(f"VIEWED PROVINCES - ({viewed_provinces})")
                buyer_province_list.extend(viewed_provinces)
                
                viewed_categories = [item["category"] for item in viewed_listings_data]
                logger.info(f"VIEWED CATEGORIES - ({viewed_categories})")
                buyer_category_list.extend(viewed_categories)
                
        # get contact seller listings
        contact_seller_listings_data = utils.sql_p_get_contacted_seller_events(buyer_email=buyer_email)
        if contact_seller_listings_data:
            contact_seller_listings = [item["mls"] for item in contact_seller_listings_data]
            logger.info(f"CONTACT SELLER LISTINGS - ({contact_seller_listings})")
            buyer_mls_list.extend(contact_seller_listings)
            
            contact_seller_listings_details: dict = utils.sql_m_get_mls_data(contact_seller_listings)
            logger.info(f"CONTACT SELLER LISTINGS DETAILS - ({contact_seller_listings_details})")
            
            if contact_seller_listings_details:
                for listing in contact_seller_listings_data:
                    mls = listing["mls"]
                    listing.update(contact_seller_listings_details[mls])

                contact_seller_provinces = [item["province"] for item in contact_seller_listings_data]
                logger.info(f"CONTACT SELLER PROVINCES - ({contact_seller_provinces})")
                buyer_province_list.extend(contact_seller_provinces)
                
                contact_seller_categories = [item["category"] for item in contact_seller_listings_data]
                logger.info(f"CONTACT SELLER CATEGORIES - ({contact_seller_categories})")
                buyer_category_list.extend(contact_seller_categories)
                
            contact_seller_listings_details_archive: dict = utils.sql_m_get_mls_data_archive(contact_seller_listings)
            logger.info(f"CONTACT SELLER ARCHIVE LISTINGS DETAILS - ({contact_seller_listings_details_archive})")
            
            if contact_seller_listings_details_archive:
                for listing in contact_seller_listings_data:
                    mls = listing["mls"]
                    listing.update(contact_seller_listings_details_archive[mls])

                contact_seller_provinces_archive = [item["province"] for item in contact_seller_listings_data]
                logger.info(f"CONTACT SELLER PROVINCES ARCHIVE - ({contact_seller_provinces_archive})")
                buyer_province_list.extend(contact_seller_provinces_archive)
                
                contact_seller_categories_archive = [item["category"] for item in contact_seller_listings_data]
                logger.info(f"CONTACT SELLER CATEGORIES ARCHIVE - ({contact_seller_categories_archive})")
                buyer_category_list.extend(contact_seller_categories_archive)
            
        buyer_mls_list = list(set(buyer_mls_list))
        logger.info(f"BUYER MLS LIST - ({buyer_mls_list})")
        
        buyer_province_list = list(set(buyer_province_list))
        logger.info(f"BUYER PROVINCE LIST - ({buyer_province_list})")
        
        buyer_category_list = list(set(buyer_category_list))
        logger.info(f"BUYER CATEGORY LIST - ({buyer_category_list})")
        
        if buyer_mls_list and (buyer_category_list or buyer_province_list):
            
            default_date_range = utils.get_default_date_range()
            
            listings = utils.sql_m_get_not_viewed_listings(
                mls_list=buyer_mls_list,
                province_list=buyer_province_list,
                category_list=buyer_category_list,
                start_date=default_date_range["start"],
                end_date=default_date_range["end"]
                )
            
    logger.info(f"BUYER NOT VIEWED LISTINGS FOUND - ({listings})")
    return {"listings": listings}
