import base64
import json
import os
from datetime import date, datetime, timedelta

import httpx
import pytz

from config import ROOT_DIR
from config.database import mysql, postgres
from config.logging_config import logger
from processors.fub import FUBProcessor
from utils import chrome_extension as utils

from . import FUB_API_KEY, FUB_BASE_URL, NINJAS_API_KEY

demo_admin = "d2lsbG93QGZiNHMuY29t"
demo_buyer = "c3RscnZua0BnbWFpbC5jb20="
demo_buyer_id = "Mjc2OTY="


def sql_m_get_buyer(buyer_email: str, buyer_chat_id: int):
    logger.info(f"GET BUYER DATA: EMAIL - {buyer_email}; CHAT ID - {buyer_chat_id}")
    # logger.warning(type(buyer_chat_id))
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
        (email = '{buyer_email}')
    OR (
            '{buyer_chat_id}' IS NOT NULL
            AND id = (
            SELECT
                sender_id
            FROM
                tbl_chat
            WHERE
                id = '{buyer_chat_id}'
            LIMIT
                1
            )
        )
        OR (
            '{buyer_email}' IS NOT NULL
            AND email = '{buyer_email}'
        )
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


def decode_base64_item(encoded_item: str) -> str | int | None:
    logger.debug(f"DECODE BASE64 - {encoded_item}")
    decoded_item = None
    if encoded_item:
        try:
            decoded_item = base64.b64decode(encoded_item).decode()
        except Exception:
            logger.exception(f"!!! FAILED DECODING - ({encoded_item}) OF TYPE ({type(encoded_item)})")
    return decoded_item


def get_utc_offset(timezone: str) -> int | None:
    logger.info(f"GET UTC OFFSET - {timezone}")
    if timezone:
        utc_now = datetime.now(pytz.utc)
        city_timezone = pytz.timezone(timezone)
        local_time = utc_now.astimezone(city_timezone)
        utc_offset = int(local_time.utcoffset().total_seconds() / 3600)
        return utc_offset
    
    
def get_timezone(city: str) -> str | None:
    logger.info(f"GET TIMEZONE FOR - {city}")
    if city:
        response = httpx.get(
            f"https://api.api-ninjas.com/v1/timezone?city={city}&country=Canada",
            headers = {"X-Api-Key": NINJAS_API_KEY}
        )
        status_code = response.status_code
        data = response.json()
        logger.info(f"NINJA API RESPONSE - {status_code} - {data}")
        if status_code == 200:
            return data["timezone"]
        
        
def sql_m_get_intro_fields(buyer_email) -> dict | None:
    logger.info(f"GET INTRO FIELDS - {buyer_email}")
    query = f"""
    select
        firstname,
        lastname,
        email,
        contact_no,
        city,
        province
    from
        tbl_customers
    where 
        email = '{buyer_email}'
    limit 1
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "first_name": raw_result[-1][0],
            "last_name": raw_result[-1][1],
            "email": raw_result[-1][2],
            "phone_number": raw_result[-1][3],
            "city": raw_result[-1][4],
            "province": raw_result[-1][5],
        }
    

def sql_m_get_complete_fields(buyer_email) -> dict | None:
    logger.info(f"GET COMPLETE FIELDS - {buyer_email}")
    query = f"""
    SELECT
        cd.area_of_intrest,
        cd.LookingBuyerType,
        cd.inteadBuy,
        cd.CashOnhand,
        cd.Location
    FROM tbl_customers c
        LEFT JOIN tbl_company_details cd
    ON c.id = cd.cust_id
        WHERE
        c.email = '{buyer_email}'
    LIMIT 1;
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "area_of_interest": raw_result[-1][0],
            "buyer_type": raw_result[-1][1],
            "purchase_time_frame": raw_result[-1][2],
            "cash_on_hand": raw_result[-1][3],
            "location": raw_result[-1][4],
        }
        
        
def sql_m_get_supplemental_business_fields(buyer_email) -> dict | None:
    logger.info(f"GET COMPLETE FIELDS - {buyer_email}")
    query = f"""
    SELECT
        cd.area_of_intrest,
        cd.LookingBuyerType,
        cd.inteadBuy,
        cd.CashOnhand,
        cd.Location
    FROM tbl_customers c
        LEFT JOIN tbl_company_details cd
    ON c.id = cd.cust_id
        WHERE
        c.email = '{buyer_email}'
    LIMIT 1;
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "area_of_interest": raw_result[-1][0],
            "buyer_type": raw_result[-1][1],
            "purchase_time_frame": raw_result[-1][2],
            "cash_on_hand": raw_result[-1][3],
            "location": raw_result[-1][4],
        }
           

def get_profile_completed_levels_algorithmic(buyer_email: str) -> dict:
    logger.info(f"GET PROFILE COMPLETED LEVELS - {buyer_email}")
    completed_levels = {
        "intro": False,
        "complete": False,
        "supplemental": False
    }
    profile_type = 1 # 1 | any - business; 2 - commercial; 3 - both
    
    # intro level
    intro_fields = sql_m_get_intro_fields(buyer_email)
    logger.info(f"INTRO FIELDS - {intro_fields}")
    if intro_fields:
        intro_completed = all(intro_fields.values())
        completed_levels["intro"] = intro_completed
        logger.info(f"INTRO COMPLTED - {intro_completed}")
    
    # complete level
    completed_fields = sql_m_get_complete_fields(buyer_email)
    logger.info(f"COMPLETE FIELDS - {completed_fields}")   
    if completed_fields:
        profile_type = completed_fields["area_of_interest"]
        
        complete_completed = all(completed_fields.values())
        completed_levels["complete"] = complete_completed
        logger.info(f"COMPLETE COMPLTED - {complete_completed}")
        
    # TODO: supplemental
    match profile_type:
        case 2:
            # commercial
            ...
        case 3:
            # both
            ...
        case _:
            # business as default
            ...
    
    return completed_levels


def sql_m_get_profile_completed_levels(buyer_email: str) -> dict | None:
    logger.info(f"GET PROFILE COMPLETED LEVELS - {buyer_email}")
    query = f"""
        select
            intro_profile_webhook_status,
            complete_profile_webhook_status,
            supplemental_profile_webhook_status
        from tbl_customers
            where email = '{buyer_email}'
        order by id desc
        limit 1
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return {
            "intro": bool(raw_result[-1][0]),
            "complete": bool(raw_result[-1][1]),
            "supplemental": bool(raw_result[-1][2]),
        }

        
if __name__ == "__main__":
    print(get_utc_offset("Toronto"))
