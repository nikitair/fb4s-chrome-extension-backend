from config.logging_config import logger
from utils import textingduncan as utils

from . import fub, twilio, retool


def send_sms(to_number: str, sms_body: str):
    sms_sending_result = twilio.send_sms(to_number, sms_body)
    return sms_sending_result.get("success", False)


def fub_note_created(note_id: int) -> dict:
    result = {
        "sms_text": None,
        "contact_name": None,
        "contact_phone": None,
        "sms_sent": False,
        "assigned_team_member_id": None,
        "sms_signature": None
    }

    # get note data
    note_data = fub.get_note(note_id)

    if note_data:
    
        # get buyer_id and note message for sms
        buyer_id = note_data["personId"]
        note_message: str = note_data["body"]
        print(note_message)
    
        # get buyer data
        buyer_data = fub.get_people(buyer_id)
    
        if buyer_data and "[scheduled]" in note_message:
    
            buyer_name = buyer_data["data"]["name"]
            result["contact_name"] = buyer_name
    
            assigned_team_member_id = buyer_data["assignedUserId"]
            result["assigned_team_member_id"] = assigned_team_member_id
    
            team_member_signature = utils.get_signature(assigned_team_member_id)
            result["sms_signature"] = team_member_signature
            note_message += team_member_signature
    
            buyer_phones = buyer_data["phones"]
            buyer_phone = buyer_phones[0]["value"] if buyer_phones and isinstance(buyer_phones, list) else None
            result["contact_phone"] = buyer_phone
    
            logger.info(f"BUYER NAME - {buyer_name}; BUYER PHONE NUMBER - {buyer_phone}")
    
            if buyer_phone:
                note_message = note_message.replace("[scheduled] ", "")
    
                # send sms
                logger.info(f"SENDING NOTE AS SMS - {note_message}")
                sending_result = twilio.send_sms(buyer_phone, note_message)
                result["sms_sent"] = sending_result["success"]
    
                # updating note
                fub.update_note(note_id=note_id, note_text=note_message)
    
        result["sms_text"] = note_message
    
    return result


def send_mailwizz_campaign_sms(campaign_special_id: int, to_phone_number: str, campaign_day: int, jerk_realtor_name: str = None, tm_name: str = None, mls: str = None):
    logger.info(f"PROCESSING MAILWIZZ CAMPAIGN DATA")

    # getting sms template if exists
    retool_response = retool.get_sms_template(campaign_special_id, campaign_day)

    if retool_response["success"] is True:

        # sending sms
        template: str = retool_response["sms_template"]
        logger.debug(f"RAW SMS TEMPLATE - {template}")

        # Jerk Realtors Logic:
        if campaign_special_id == 9:
            logger.info(f"JERK REALTORS LOGIC")

            logger.info(f"TM NAME - {tm_name}")
            logger.info(f"MLS - {mls}")
            logger.info(f"JR NAME - {jerk_realtor_name}")

            match campaign_day:
                case 1:
                    template = template.replace('zzzzz', tm_name)
                    template = template.replace('xxxxx', mls)

                case 2:
                    template = template.replace('yyyyy', jerk_realtor_name)

                case _:
                    pass
        
        logger.info(f"SMS TEMPLATE TO SEND - {template}; RECEIVER - {to_phone_number}")
        return send_sms(to_phone_number, template)
