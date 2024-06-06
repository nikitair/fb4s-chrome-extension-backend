from fastapi import APIRouter, Query
from config.logging_config import logger

from schemas.index import DefaultResponse
from schemas.tools import Base64Response
from services import tools as services

tools_router = APIRouter()


@tools_router.get("/", response_model=DefaultResponse)
async def tools_index():
    return {
        "success": True,
        "service": "fb4s-automations",
        "router": "tools",
    }

@tools_router.post("/base64/encode/")
async def encode_to_base64(
        item = Query(description="Item to be encoded")
    ) -> Base64Response:
    logger.info("*** ENCODE TO BASE64 TRIGGERED")
    return services.encode_to_base64(item)


@tools_router.post("/base64/decode/")
async def decode_from_base64(
        item = Query(description="Item to be decoded")
    ) -> Base64Response:
    logger.info("*** DECODE FROM BASE64 TRIGGERED")
    return services.encode_to_base64(item)



