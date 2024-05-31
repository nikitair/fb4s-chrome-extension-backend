from config.logging_config import logger
from config.database import mysql
from utils import chrome_extension as utils
import json
import os
from config import ROOT_DIR


def sql_m_get_buyer(buyer_email: str, buyer_customer_id: int):
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
    logger.debug(f"GETTING BUYER: EMAIL - ({buyer_email}); ID - {buyer_customer_id}")
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
    
        

def sql_m_check_if_rca_signed(viewer_email: str, buyer_email: str) -> bool:
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
    logger.debug(f"CHECKING IF RCA SIGNED: VIEWER - {viewer_email}; BUYER - {buyer_email}")
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    return True if raw_result else False


def sql_p_get_buyer_lead_score(buyer_email: str):
    query = f"""
    SELECT
        res5."Email",
        res5."Infinite Lead Score",
        -- MAX(conversions.decimal_value) AS "Decimal Lead Score",
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
                            -- AND events.time BETWEEN '{{dateRange3.value.start}}' AND '{{dateRange3.value.end}}'
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
            -- decimal_value,
            five_star_value
        FROM
            statistics.event_scoring_conversion
        ORDER BY
            thousand_value DESC
    ) AS conversions ON res5."Infinite Lead Score" >= conversions.thousand_value
        WHERE res5."Email" = '{buyer_email}'
    GROUP BY
    """
    logger.debug(f"GETTING LEAD SCORE - {buyer_email}")
    raw_result = mysql.execute_with_connection(
        func=mysql.select_executor,
        query=query
    )
    return raw_result
  


def get_buyer_profile(access_level_key: str = None, profile_ekey: str = None, profile_ikey: str = None) -> dict | None:
    viewer_email = utils.decode_base64_item(access_level_key)
    buyer_email = utils.decode_base64_item(profile_ekey)
    buyer_customer_id = utils.decode_base64_item(profile_ikey)
    
    # getting buyer data
    buyer_data = sql_m_get_buyer(buyer_email, buyer_customer_id)
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
        
        # checking viewer permission
        if check_if_viewer_is_admin(viewer_email):
            result["show_contacts"] = True
            logger.info("VIEWER IS ADMIN")
        else:
            result["show_contacts"] = sql_m_check_if_rca_signed(viewer_email, buyer_email)
            
        # evaluating buyer lead score
        # lead_score = sql_p_get_buyer_lead_score(buyer_email)
        # logger.info(f"BUYER LEAD SCORE - {lead_score}")
    
        return result
