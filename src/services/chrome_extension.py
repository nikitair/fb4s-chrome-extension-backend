from config.logging_config import logger
from config.database import mysql
from utils import chrome_extension as utils
import json
import os
from config import ROOT_DIR


def sql_get_buyer(buyer_email: str, buyer_customer_id: int):
    query = f"""
    SELECT
        id,
        email,
        contact_no,
        firstname,
        lastname
    FROM 
        tbl_customers
    WHERE 
        email = '{buyer_email}'
    OR 
        id = '{buyer_customer_id}'
    ORDER BY id DESC
    LIMIT 1
    """
    logger.info(f"GETTING BUYER: EMAIL - ({buyer_email}); ID - {buyer_customer_id}")
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "buyer_id": raw_result[-1][0],
            "buyer_email": raw_result[-1][1],
            "buyer_phone_number": raw_result[-1][2],
            "buyer_first_name": raw_result[-1][3],
            "buyer_last_name": raw_result[-1][4]
        }
        
        
def check_if_viewer_is_admin(viewer_email: str) -> bool:
    logger.info(f"CHECKING IF VIEWER IS ADMIN - {viewer_email}")
    admin_emails_path = os.path.join(ROOT_DIR, "src", "database", "admins.json")
    admin_emails = []
    
    with open(admin_emails_path, "r") as f:
        admin_emails = json.load(f)
        
    return viewer_email in admin_emails
    
        

def sql_check_if_rca_signed(viewer_email: str, buyer_email: str) -> bool:
    query=f"""
    SELECT
        id
    FROM
        tbl_agreement_details
    WHERE
        receiving_broker_email = '{viewer_email}'
    AND
        referred_buyer_email = '{buyer_email}'
    AND
        type IN (2, 3)
    LIMIT
        1
    """
    logger.info(f"CHECKING IF RCA SIGNED: VIEWER - {viewer_email}; BUYER - {buyer_email}")
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    return True if raw_result else False
  


def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None) -> dict | None:
    viewer_email = utils.decode_base64_item(access_level_key)
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_customer_id = utils.decode_base64_item(profile_ikey)
    
    # get buyer data
    buyer_data = sql_get_buyer(buyer_email, buyer_customer_id)
    logger.info(f"BUYER DATA - {buyer_data}")
    
    if buyer_data:
        result = {
            "buyer_id": buyer_data["buyer_id"],
            "buyer_email": buyer_data["buyer_email"],
            "buyer_phone_number": buyer_data["buyer_phone_number"],
            "buyer_first_name": buyer_data["buyer_first_name"],
            "buyer_last_name": buyer_data["buyer_last_name"],
            "show_contacts": False
        }
        
        if check_if_viewer_is_admin(viewer_email):
            result["show_contacts"] = True
            logger.info("VIEWER IS ADMIN")
        else:
            result["show_contacts"] = sql_check_if_rca_signed(viewer_email, buyer_email)
    
        return result
