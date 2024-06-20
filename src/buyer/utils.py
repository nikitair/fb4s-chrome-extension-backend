import base64
import json
import os
from datetime import date, datetime, timedelta

import httpx
import pytz

from config import ROOT_DIR
from config.database import mysql, postgres
from config.logging_config import logger
from fub.services import FUBService

from . import FUB_API_KEY, FUB_BASE_URL, NINJAS_API_KEY

demo_admin = "d2lsbG93QGZiNHMuY29t"
demo_buyer = "c3RscnZua0BnbWFpbC5jb20="
demo_buyer_id = "Mjc2OTY="


def sql_m_get_buyer(buyer_email: str, buyer_chat_id: int) -> dict | None:
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
    fub = FUBService(api_key=FUB_API_KEY, base_url=FUB_BASE_URL)
    buyer_data = fub.get_person_by_email(buyer_email)
    if buyer_data:
        fub_stage = buyer_data[0]["stage"]
        return fub_stage
    else:
        return "Not a FUB Buyer"
    

def sql_m_get_buyer_assigned_realtor(buyer_email: str):
    logger.info(f"GET ASSIGNED REALTOR OF - {buyer_email}")
    query = f"""
        SELECT
            agreement.receiving_broker_first_name,
            agreement.receiving_broker_last_name,
            agreement.receiving_broker_email,
            customers.email,
            customers.id as customers_id,
            fub.broker_id,
            fub.broker_external_id
        FROM
            tbl_agreement_details agreement
        LEFT JOIN tbl_customers customers 
            ON agreement.receiving_broker_email = customers.email
        LEFT JOIN tbl_external_crm_leads fub 
            ON fub.broker_id = customers.id
        WHERE
            agreement.referred_buyer_email = '{buyer_email}'
        ORDER BY 
            agreement.date_referral_agreement DESC
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
        logger.info(f"STATUS CODE - {status_code}")
        if status_code == 200:
            data = response.json()
            logger.info(f"NINJA API RESPONSE - {data}")
            if status_code == 200:
                return data["timezone"]
        else:
            logger.error(f"NINJA API ERROR - {response.text}")
        
        
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
            "supplemental": bool(raw_result[-1][2])
        }
        
        
def sql_m_get_chat_id(buyer_id: int) -> int | None:
    logger.info(f"GET CHAT ID FOR - {buyer_id}")
    query = f"""
    SELECT
        id
    FROM
        tbl_chat
    WHERE
        sender_id = {buyer_id}
    AND 
        message_flag = "first_message"
    ORDER BY 
        created_at ASC
    LIMIT 1
    """
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    if raw_result:
        return raw_result[-1][0]
    
    
def prepare_sign_rca_link(buyer_id) -> str:
    logger.info(f"PREPARE SIGN RCA FORM URL FOR - {buyer_id}")
    sign_rca_url = "https://www.findbusinesses4sale.com/"
    chat_id = sql_m_get_chat_id(buyer_id)
    logger.info(f"BUYER CHAT ID - {chat_id}")
    if chat_id:
        lead_id = {
            "chat_id":chat_id,
            "connection_owner_id":"18705"
        }
        try:
            jsonstr_lead_id = json.dumps(lead_id)
            base64_lead_id = base64.b64encode(jsonstr_lead_id.encode()).decode()
            sign_rca_url += f"rca/{base64_lead_id}"
        except (TypeError, ValueError) as e:
            logger.exception(f"!!! FAILED ENCODING LEAD_ID - {e}")
    return sign_rca_url

        

def sql_m_get_buyer_leads(buyer_id: int) -> list:
    logger.info(f"SQL GET LEADS OF - ({buyer_id})")
    query = f"""
        SELECT
            tbl_advertisement.DDF_ID AS MLS,
            tbl_advertisement.search_city AS city,
            tbl_advertisement.search_province AS province,
            tbl_advertisement.zip_code AS postal_code,
            tbl_advertisement.compiled_category_name AS category,
            tbl_advertisement.address AS address,
            tbl_advertisement.askingpricesorting AS price,
            tbl_advertisement.latitude_val AS latitude,
            tbl_advertisement.longitude_val AS longitude
        FROM
            tbl_chat
        INNER JOIN 
            tbl_advertisement 
        ON 
            tbl_chat.listing_id = tbl_advertisement.id
        WHERE
            sender_id = '{buyer_id}'
        AND 
            message_flag = 'first_message'
        ORDER BY
            tbl_advertisement.askingpricesorting 
        DESC;
    """
    leads = []
    raw_response = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            leads.append(
                {
                    "mls": item[0],
                    "city": item[1],
                    "province": item[2],
                    "postal_code": item[3],
                    "category": item[4],
                    "address": item[5],
                    "price": item[6],
                    "latitude": item[7],
                    "longitude": item[8]
                }
            )
    return leads


def sql_p_get_in_person_evaluation(buyer_email: str) -> list:
    logger.info(f"SQL GET IN-PERSON EVALUATIONS - ({buyer_email})")
    query = f"""
        SELECT
            call_event,
            evaluator_type,
            evaluating_person as evaluator_name,
            mark,
            comment,
            evaluating_datetime as date
        FROM
            statistics.retool_person_evaluation
        WHERE
            email = '{buyer_email}'
        ORDER BY
            evaluating_datetime 
        DESC
    """
    evaluations = []
    raw_response = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            evaluations.append(
                {
                    "call_event": item[0],
                    "evaluator_type": item[1],
                    "evaluator_name": item[2],
                    "mark": item[3],
                    "comment": item[4],
                    "date": item[5]
                }
            )
    return evaluations


def sql_p_get_leads_score_events(buyer_email: str) -> list:
    logger.info(f"SQL GET LEAD SCORE EVENTS - ({buyer_email})")
    query = f"""
        SELECT
            "Event Name",
            "Events Amount",
            "Event Score",
            "All Events Score",
            "Total Score",
        MAX(conversions.five_star_value) AS "Five Star Score"
        FROM
        (
        SELECT
        *,
        "All Events Score" + "Bonus for High Interest" + "Bonus for Price" AS "Total Score"
        FROM
        (
            SELECT
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
                "Event Name",
                "MLS",
                CASE
                    WHEN MAX("Listing Price") is not null THEN MAX("Listing Price")::DECIMAL
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
                    fb4s_users."User Type" AS "User Type",
                    events.event AS "Event Name",
                    events."MLS" AS "MLS",
                    events."Listing Price" AS "Listing Price",
                    scoring.score AS "Event Score"
                    FROM
                    marketing_ecosystem.mixpanel_to_aws.engage AS fb4s_users
                    INNER JOIN marketing_ecosystem.mixpanel_to_aws.export AS events ON fb4s_users.id = events.id
                    INNER JOIN marketing_ecosystem.statistics.lead_scoring AS scoring ON events.event = scoring.event_name
                    WHERE
                    fb4s_users.id = '{buyer_email}'
                ) res
                GROUP BY
                "Event Name",
                "MLS",
                "Event Score"
            ) res_2
            GROUP BY
            "Event Name",
            "Event Score"
        ) res_3
        ORDER BY
        "Total Score" DESC
        ) ts
        INNER JOIN (
            SELECT
            thousand_value,
            five_star_value
            FROM
            statistics.event_scoring_conversion
            ORDER BY
            thousand_value DESC
        ) AS conversions ON ts."Total Score" >= conversions.thousand_value
        GROUP BY
        ts."Event Name",
        ts."Events Amount",
        ts."Event Score",
        ts."All Events Score",
        ts."Total Score"
        ORDER BY
        ts."Total Score" DESC;
    """
    events = []
    raw_response = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            events.append(
                {
                    "event": item[0],
                    "events_amount": item[1],
                    "event_score": item[2],
                    "all_events_score": item[3],
                    "total_score": item[4]
                }
            )
    return events


def sql_m_get_mls_data(mls_list: list) -> dict:
    logger.info(f"SQL GET MLS DATA - ({mls_list})")
    query = f"""
        SELECT
            tbl_advertisement.DDF_ID AS `MLS`,
            tbl_advertisement.city AS `City`,
            tbl_advertisement.province AS `Province`,
            tbl_advertisement.compiled_category_name AS `Category`,
            ListingCategories AS `Tags`,
            tbl_advertisement.AskingPriceSorting AS `Price`,
            CONCAT(realtor.firstname, ' ', realtor.lastname) AS `Assigned Realtor Full Name`,
            realtor.email AS `Assigned Realtor Email`,
            realtor.contact_no AS `Assigned Realtor Phone`,
            internal_url AS listing_url
        FROM
            tbl_advertisement
        LEFT JOIN 
            tbl_customers realtor 
                ON realtor.id = tbl_advertisement.user_id
            WHERE
        DDF_ID in %s
    """
    mls_data = {}
    raw_response = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query,
        params = tuple(mls_list)
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            mls_data[item[0]] = {
                    "mls": item[0],
                    "city": item[1],
                    "province": item[2],
                    "category": item[3],
                    "tags": item[4],
                    "price": item[5],
                    "assigned_realtor_name": item[6],
                    "assigned_realtor_email": item[7],
                    "assigned_realtor_phone": item[8],
                    "listing_url": item[9],
                    "image_url": f"https://cdn.repliers.io/crea2/IMG-{item[0]}_1.jpg?w=730&f=webp",
                }
            
    return mls_data


def sql_m_get_mls_data_archive(mls_list: list) -> dict:
    logger.info(f"SQL GET ARCHIVE MLS DATA - ({mls_list})")
    query = f"""
        SELECT
            tbl_advertisement.DDF_ID AS `MLS`,
            tbl_advertisement.city AS `City`,
            tbl_advertisement.province AS `Province`,
            tbl_advertisement.compiled_category_name AS `Category`,
            ListingCategories AS `Tags`,
            tbl_advertisement.AskingPriceSorting AS `Price`,
            CONCAT(realtor.firstname, ' ', realtor.lastname) AS `Assigned Realtor Full Name`,
            realtor.email AS `Assigned Realtor Email`,
            realtor.contact_no AS `Assigned Realtor Phone`,
            internal_url AS listing_url
        FROM
            tbl_archive_listings
        LEFT JOIN 
            tbl_customers realtor 
                ON realtor.id = tbl_advertisement.user_id
            WHERE
        DDF_ID in %s
    """
    mls_data = {}
    raw_response = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query,
        params = tuple(mls_list)
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            mls_data[item[0]] = {
                    "mls": item[0],
                    "city": item[1],
                    "province": item[2],
                    "category": item[3],
                    "tags": item[4],
                    "price": item[5],
                    "assigned_realtor_name": item[6],
                    "assigned_realtor_email": item[7],
                    "assigned_realtor_phone": item[8],
                    "listing_url": item[9],
                    "image_url": f"https://cdn.repliers.io/crea2/IMG-{item[0]}_1.jpg?w=730&f=webp",
                }
            
    return mls_data


def sql_p_get_buyer_mixpanel_email(buyer_email: str) -> str | None:
    logger.info(f"SQL GET BUYER MIXPANEL EMAIL - ({buyer_email})")
    query = f"""
        SELECT 
            distinct_id as mixpanel_email 
        FROM 
            mixpanel_to_aws.engage
        WHERE 
            id = '{buyer_email}'
    """
    raw_response = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        return raw_response[0][0]


def sql_p_get_contacted_seller_events(buyer_email: str) -> list:
    logger.info(f"SQL GET CONTACTED SELLER EVENTS - ({buyer_email})")
    query = f"""
        SELECT
            "MLS",
            MAX(time) AS "Time"
        FROM
            marketing_ecosystem.mixpanel_to_aws.export
        WHERE
            event = 'Contact Seller'
        AND id = '{buyer_email}'
        GROUP BY
            "MLS"
    """
    contacted_seller_events = []
    raw_response = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            contacted_seller_events.append(
                {
                    "mls": item[0],
                    "event_date": item[1]
                }
            )
    return contacted_seller_events


def sql_p_get_all_green_button_click_events(buyer_email: str) -> list:
    logger.info(f"SQL GET ALL GREEN BUTTON CLICKS EVENTS - ({buyer_email})")
    query = f"""
        SELECT
            "MLS",
            MIN(time) AS time
        FROM
            marketing_ecosystem.mixpanel_to_aws.export
        WHERE
            (
                event = 'Listing: Contact Seller button' 
            OR 
                event = 'Search page: Contact Seller button' 
            OR 
                event = 'Contact Seller'
            )
        AND (
            id = '{buyer_email}'
        OR
            distinct_id = '{buyer_email}'
            )
        GROUP BY "MLS";
    """
    events = []
    raw_response = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            events.append(
                {
                    "mls": item[0],
                    "event_date": item[1]
                }
            )
    return events


def sql_p_get_view_listing_events(buyer_email: str) -> list:
    logger.info(f"SQL GET VIEW LISTING EVENTS - ({buyer_email})")
    query = f"""
        SELECT
            "MLS",
            COUNT("MLS") AS "Views Amount",
            MAX(time) AS "Last View Time"
        FROM
            marketing_ecosystem.mixpanel_to_aws.export
        WHERE
            event = 'View Listing'
        AND (
            id = '{buyer_email}'
        OR
            distinct_id = '{buyer_email}'
            )
        GROUP BY
            "MLS"
        ORDER BY
            "Views Amount" DESC
    """
    events = []
    raw_response = postgres.execute_with_connection(
        func=postgres.select_executor,
        query=query
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            events.append(
                {
                    "mls": item[0],
                    "views_amount": item[1],
                    "event_date": item[2]
                }
            )
    return events


def sql_m_get_buyer_categories(buyer_mls_list: list) -> list:
    logger.info(f"SQL GET BUYER CATEGORIES - ({buyer_mls_list})")
    query = f"""
        SELECT
            `Category`,
            SUM(`Amount`) AS `Listings Amount`,
            ROUND(MIN(`Price`), 0) AS `Minimum Price`,
            ROUND(SUM(`Total`) / SUM(`Amount`), 0) AS `Average Price`,
            ROUND(MAX(`Price`), 0) AS `Maximum Price`
        FROM
        (
            SELECT
            `Category`,
            `Price`,
            COUNT(*) AS `Amount`,
            `Price` * COUNT(*) AS `Total`
            FROM
            (
                SELECT
                    compiled_category_name AS `Category`,
                AskingPriceSorting AS `Price`
                FROM
                    tbl_advertisement
                WHERE
                DDF_ID in %s
            ) res
            GROUP BY
            `Category`,
            `Price`
        ) res2
        GROUP BY
        `Category`
        ORDER BY
        `Listings Amount` DESC
        
        UNION
        
        SELECT
            `Category`,
            SUM(`Amount`) AS `Listings Amount`,
            ROUND(MIN(`Price`), 0) AS `Minimum Price`,
            ROUND(SUM(`Total`) / SUM(`Amount`), 0) AS `Average Price`,
            ROUND(MAX(`Price`), 0) AS `Maximum Price`
        FROM
        (
            SELECT
            `Category`,
            `Price`,
            COUNT(*) AS `Amount`,
            `Price` * COUNT(*) AS `Total`
            FROM
            (
                SELECT
                    compiled_category_name AS `Category`,
                AskingPriceSorting AS `Price`
                FROM
                    tbl_archive_listings
                WHERE
                DDF_ID in %s
            ) res
            GROUP BY
            `Category`,
            `Price`
        ) res2
        GROUP BY
        `Category`
        ORDER BY
        `Listings Amount` DESC
    """
    categories = []
    raw_response = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query,
        params = tuple(buyer_mls_list)
    )
    logger.info(f"SQL RAW RESPONSE - ({raw_response})")
    if raw_response:
        for item in raw_response:
            categories.append(
                {
                    "category": item[0],
                    "listings_amount": item[1],
                    "min_price": item[2],
                    "avg_price": item[3],
                    "max_price": item[4]
                }
            )
            
    return categories
