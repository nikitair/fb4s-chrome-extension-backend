from fastapi import APIRouter

from config.logging_config import logger
from schemas.index import DefaultResponse
from schemas.textingduncan import FUBNoteCreated, FUBNoteCreatedResponse
from services import textingduncan as services

td_router = APIRouter()


@td_router.get("/", response_model=DefaultResponse)
async def td_index_view():
    return {
        "success": True,
        "service": "FB4S Automations",
        "router": "textingduncan",
    }


@td_router.post("/fub/note-created/", response_model=FUBNoteCreatedResponse)
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
