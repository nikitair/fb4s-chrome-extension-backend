import json
import os
from datetime import date, timedelta
from . import (FUB_API_KEY, FUB_BASE_URL)
from processors.fub import FUBProcessor

from fastapi.responses import JSONResponse

from config import ROOT_DIR
from config.database import mysql, postgres
from config.logging_config import logger
from utils import chrome_extension as utils

from schemas import chrome_extension as schemas


def sql_m_get_buyer(buyer_email: str, buyer_customer_id: int):
    logger.info(f"GET BUYER DATA: EMAIL - {buyer_email}; ID - {buyer_customer_id}")
    query = f"""
    SELECT
        id,
        email,
        contact_no,
        firstname,
        lastname,
        city,
        province,
        registered_at
    FROM 
        tbl_customers
    WHERE 
        email = '{buyer_email}'
    OR 
        id = '{buyer_customer_id}'
    ORDER BY id DESC
    LIMIT 1
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "id": raw_result[-1][0],
            "email": raw_result[-1][1],
            "phone_number": raw_result[-1][2],
            "first_name": raw_result[-1][3],
            "last_name": raw_result[-1][4],
            "city": raw_result[-1][5],
            "province": raw_result[-1][6],
            "registration_time": raw_result[-1][7]
        }
    else:
        logger.warning("NO BUYER FOUND")
        
        
def check_if_viewer_is_admin(viewer_email: str) -> bool:
    logger.info(f"CHECK IF VIEWER IS ADMIN - {viewer_email}")
    admin_emails_path = os.path.join(ROOT_DIR, "src", "database", "admins.json")
    admin_emails = []
    with open(admin_emails_path, "r") as f:
        admin_emails = json.load(f)
    return viewer_email in admin_emails
     

def sql_m_check_if_rca_signed(viewer_email: str, buyer_email: str) -> bool:
    logger.info(f"CHECK IF RCA SIGNED: TEAM MEMBER - {viewer_email}; BUYER - {buyer_email}")
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
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    return True if raw_result else False


def sql_p_get_buyer_lead_score(buyer_email: str):
    logger.info(f"GET BUYER LEAD SCORE - {buyer_email}")
    query = f"""
    SELECT
    -- res5."Email",
    -- res5."Infinite Lead Score",
    MAX(conversions.five_star_value) AS "Five Star Score"
    FROM
    (
        SELECT
        "Email",
        SUM("Total Score") AS "Infinite Lead Score"
        FROM
        (
            SELECT
            *,
            "All Events Score" + "Bonus for High Interest" + "Bonus for Price" AS "Total Score"
            FROM
            (
                SELECT
                "Email",
                "Event Name",
                COUNT("Event Name") AS "Events Amount",
                "Event Score",
                COUNT("Event Name") * "Event Score" AS "All Events Score",
                SUM("Event Amount > 3") * 300 AS "Bonus for High Interest",
                ROUND(AVG("Listing Price")::numeric, 0) AS "Average Price",
                CASE
                    WHEN ROUND(AVG("Listing Price")::numeric, 0) >= 500000
                    AND ROUND(AVG("Listing Price")::numeric, 0) < 1000000 THEN 300
                    WHEN ROUND(AVG("Listing Price")::numeric, 0) >= 1000000 THEN 500
                    ELSE 0
                END AS "Bonus for Price"
                FROM
                (
                    SELECT
                    "Email",
                    "Event Name",
                    "MLS",
                    CASE
                        WHEN MAX("Listing Price") IS NOT NULL THEN MAX("Listing Price")::DECIMAL
                        ELSE 0
                    END AS "Listing Price",
                    COUNT("MLS") AS "Event Amount",
                    "Event Score",
                    SUM("Event Score") AS "Total Score by Event",
                    CASE
                        WHEN COUNT("MLS") > 3 THEN 1
                        ELSE 0
                    END AS "Event Amount > 3"
                    FROM
                    (
                        SELECT
                        fb4s_users.id AS "Email",
                        events.event AS "Event Name",
                        events."MLS" AS "MLS",
                        events."Listing Price" AS "Listing Price",
                        scoring.score AS "Event Score"
                        FROM
                        marketing_ecosystem.mixpanel_to_aws.engage AS fb4s_users
                        INNER JOIN marketing_ecosystem.mixpanel_to_aws.export AS events ON fb4s_users.id = events.id
                        INNER JOIN marketing_ecosystem.statistics.lead_scoring AS scoring ON events.event = scoring.event_name
                        WHERE
                        COALESCE(fb4s_users."User Type", fb4s_users.user_type) = 'buyer'
                        AND events.time BETWEEN '{(date.today() - timedelta(days=30)).isoformat()}' AND '{date.today().isoformat()}'
                    ) res
                    GROUP BY
                    "Email",
                    "Event Name",
                    "MLS",
                    "Event Score"
                ) res_2
                GROUP BY
                "Email",
                "Event Name",
                "Event Score"
            ) res3
        ) res4
        GROUP BY
        "Email"
    ) res5
    INNER JOIN (
        SELECT
        thousand_value,
        five_star_value
        FROM
        statistics.event_scoring_conversion
        ORDER BY
        thousand_value DESC
    ) AS conversions ON res5."Infinite Lead Score" >= conversions.thousand_value
        WHERE res5."Email" = '{buyer_email}'
    GROUP BY
    res5."Email",
    res5."Infinite Lead Score"
    ORDER BY
    res5."Infinite Lead Score" DESC;
    """
    raw_result = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    return raw_result[-1][0] if raw_result else 0


def get_buyer_fub_stage(buyer_email):
    logger.info(f"GET BUYER FUB STAGE - {buyer_email}")
    fub = FUBProcessor(api_key=FUB_API_KEY, base_url=FUB_BASE_URL)
    buyer_data = fub.get_person_by_email(buyer_email)
    if buyer_data:
        fub_stage = buyer_data[0]["stage"]
        return fub_stage
    else:
        return "Not a FUB Buyer"
    

def sql_m_get_buyer_assigned_realtor(buyer_email: str):
    logger.info(f"GET ASSIGNED REALTOR - {buyer_email}")
    query = f"""
        SELECT
            agreement.receiving_broker_first_name as realtor_first_name,
            agreement.receiving_broker_last_name as realtor_last_name,
            agreement.receiving_broker_email as realtor_email
        FROM
            tbl_agreement_details agreement
        LEFT JOIN tbl_customers customers 
            ON agreement.receiving_broker_email = customers.email
        LEFT JOIN tbl_external_crm_leads fub 
            ON fub.broker_id = customers.id
        WHERE
            agreement.referred_buyer_email = 'drewkuhn96@gmail.com'
        ORDER BY agreement.date_referral_agreement DESC
            LIMIT 1
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "assigned_realtor_name": (raw_result[-1][0] + ' ' + raw_result[-1][1]),
            "assigned_realtor_email": raw_result[-1][2]
        }
  
  
def sql_p_get_predefigned_location(buyer_id: int):
    logger.info(f"GET PREDEFIGNED LOCATION: BUYER ID - {buyer_id}")
    query = f"""
        SELECT
            mp_reserved_city AS city,
            mp_reserved_region AS province,
            mp_reserved_timezone AS timezone
        FROM
            mixpanel_to_aws.engage
        WHERE
            id = '{buyer_id}'
    """
    raw_result = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    if raw_result:
        return {
            "city": raw_result[-1][0],
            "province": raw_result[-1][1],
            "timezone": raw_result[-1][2]
        }


def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None) -> dict | None:
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
        "buyer_time_zone": 0,
        "lead_score": None,
        "assigned_realtor_name": None,
        "assigned_realtor_email": None,
        "profile_completed_levels": {
            "intro": False,
            "complete": False,
            "supplemental": False
        },
        "show_contacts": False
    }
    
    viewer_email = utils.decode_base64_item(access_level_key)
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_customer_id = utils.decode_base64_item(profile_ikey)
    
    logger.info(f"access_level_key = {access_level_key} -> {viewer_email}")
    logger.info(f"profile_ekey = {profile_ekey} -> {buyer_email}")
    logger.info(f"profile_ikey = {profile_ikey} -> {buyer_customer_id}")
    
    # get buyer data
    buyer_data = sql_m_get_buyer(buyer_email, buyer_customer_id)
    logger.info(f"BUYER DATA - {buyer_data}")
    
    if buyer_data:
        buyer_profile.update(buyer_data)
    
        # checking viewer permission
        viewer_is_admin = check_if_viewer_is_admin(viewer_email)
        if viewer_is_admin:
            buyer_profile["show_contacts"] = True
        else:
            rca_signed = sql_m_check_if_rca_signed(viewer_email, buyer_email)
            buyer_profile["show_contacts"] = rca_signed
            logger.info(f"RCA SIGNED - {rca_signed}")
            
        # evaluating buyer lead score
        lead_score = sql_p_get_buyer_lead_score(buyer_email)
        buyer_profile["lead_score"] = lead_score
        logger.info(f"BUYER LEAD SCORE - {lead_score}")
        
        # get fub stage
        buyer_fub_stage = get_buyer_fub_stage(buyer_email)
        buyer_profile["fub_stage"] = buyer_fub_stage
        logger.info(f"BUYER FUB STAGE - {buyer_fub_stage}")
        
        # get assigned realtor
        assigned_reator_data = sql_m_get_buyer_assigned_realtor(buyer_email)
        logger.info(f"ASSIGNED REATOR - {assigned_reator_data}")
        if assigned_reator_data:
            buyer_profile["assigned_realtor_email"] = assigned_reator_data["assigned_realtor_email"]
            buyer_profile["assigned_realtor_name"] = assigned_reator_data["assigned_realtor_name"]
            
        # get buyer UTC offset 
        buyer_predefigned_location = sql_p_get_predefigned_location(buyer_profile["id"])
        if buyer_predefigned_location:
            timezone = buyer_predefigned_location["timezone"]
            utc_offset = utils.get_utc_offset(timezone)
            buyer_profile["buyer_time_zone"] = utc_offset
            logger.info(f"BUYER TIME ZONE - {timezone}; UTC OFFSET - {utc_offset}")
        
    return buyer_profile
