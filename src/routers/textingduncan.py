from fastapi import APIRouter
from fastapi import Request

from config.logging_config import logger
from schemas.index import DefaultResponse
from schemas.textingduncan import (FUBNoteCreated, FUBNoteCreatedResponse,
                                   SendSMS, SendSMSResponse, MailWizzWebhook, MailWizzWebhookResponse)
from services import textingduncan as services

td_router = APIRouter()


@td_router.get("/", response_model=DefaultResponse)
async def td_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "textingduncan",
    }


@td_router.post("/sms/send-sms/", response_model=SendSMSResponse)
async def send_sms_view(request: SendSMS):
    payload = dict(request)
    logger.debug(f"PAYLOAD RECEIVED - {payload}")
    to_number = payload.get("to_number")
    sms_body = payload.get("sms_body")

    result = {
        "success": False,
        "to_phone_number": to_number,
        "sms_message": sms_body
    }

    is_sent = services.send_sms(to_number, sms_body)

    if is_sent:
        logger.info(f"SMS SUCCESSFULLY SENT TO - {to_number}")
        result["success"] = True
    else:
        logger.error(f"! FAILED SENDING SMS TO - {to_number}")

    return result


@td_router.post("/sms/fub/note-created/", response_model=FUBNoteCreatedResponse)
async def fub_note_created_webhook(request: FUBNoteCreated):
    """
    {
    'eventId': '3f692eb1-cd1d-411b-a3eb-9c811c22bc92',
    'eventCreated': '2024-05-27T12:14:14+00:00',
    'event': 'notesCreated',
    'resourceIds': [30189],
    'uri': 'https://api.followupboss.com/v1/notes/30189'}
    """
    result = dict()
    payload = dict(request)
    logger.debug(f"RAW PAYLOAD - {payload}")

    note_ids: list = payload["resourceIds"]
    if note_ids and isinstance(note_ids, list):
        result = services.fub_note_created(list(set(note_ids))[-1])
        logger.info(f"NOTE PROCESSING RESPONSE DATA - {result}")

    return {
        "success": result.get("sms_sent", False),
        "data": result
    }



@td_router.post("/sms/mailwizz", response_class=MailWizzWebhookResponse)
async def mailwizz_webhook_view(request: MailWizzWebhook):

    result = {
        "success": False,
        "sms_template": None
    }

    payload = dict(request)
    logger.info(f"PAYLOAD RECEIVED - {payload}")

    campaign_special_id = payload["campaign_special_id"]
    to_phone_number = payload["phone_number"]
    campaign_day = payload["campaign_day"]

    # Jerk Realtors Logic
    jerk_realtor_name = payload.get("jerk_realtor_name", "Realtor")
    tm_name = payload.get("tm_name", "Willow Graznow")
    mls = payload.get("mls", "N/A")

    service_result = services.send_mailwizz_campaign_sms(
        campaign_special_id, 
        to_phone_number, 
        campaign_day,
        jerk_realtor_name,
        tm_name,
        mls
    )
    if service_result:
        result["success"] = True
        result["sms_template"] = service_result

    return result
