from fastapi import APIRouter

from config.logging_config import logger
from schemas.index import DefaultResponse
from schemas.textingduncan import FUBNoteCreated, FUBNoteCreatedResponse, SendSMS, SendSMSResponse
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
async def td_fub_note_created_webhook(request: FUBNoteCreated):
    result = dict()
    payload = dict(request)
    logger.debug(f"RAW PAYLOAD - {payload}")

    note_ids = payload["resourceIds"]
    if note_ids:
        result = services.fub_note_created(note_ids[0])
        logger.info(f"NOTE PROCESSING RESPONSE DATA - {result}")

    return {
        "success": result.get("sms_sent", False),
        "data": result
        }



