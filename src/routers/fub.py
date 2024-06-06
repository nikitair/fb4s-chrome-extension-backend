from fastapi import APIRouter, Query
from config.logging_config import logger

from schemas.index import DefaultResponse
from schemas import fub as schemas
from services import fub as services

fub_router = APIRouter()


@fub_router.get("/", response_model=DefaultResponse)
async def fub_index():
    return {
        "success": True,
        "service": "fb4s-automations",
        "router": "fub",
    }

# @fub_router.get(
#     path="/people/{person_id}",
#     responses={
#         200: schemas.FUBItemResponse,
#         404: schemas.NoFoundResponse
#     }
# )
# async def get_person_by_id(person_id: int):
#     logger.info("*** GET FUB PERSON BY ID TRIGGERED")
#     return services.get_person(person_id)


# @fub_router.get(
#     path="/users/{user_id}",
#     responses={
#         200: schemas.FUBItemResponse,
#         404: schemas.NoFoundResponse
#     }
# )
# async def get_user_by_id(user_id: int):
#     logger.info("*** GET FUB USER BY ID TRIGGERED")
#     return services.get_user(user_id)
