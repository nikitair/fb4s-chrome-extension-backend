from fastapi import APIRouter, Query

from config.logging_config import logger
from buyer_comm_panel import schemas
from buyer_comm_panel import services
from buyer_comm_panel import utils

router = APIRouter()


@router.post("/successfully-contacted")
async def successfully_contacted(request: schemas.SuccessfullyContacted) -> schemas.CallEventResponse:
    ...
