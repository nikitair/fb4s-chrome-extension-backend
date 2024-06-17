from config.logging_config import logger
from processors.fub import FUBProcessor
from schemas import fub as schemas
from . import FUB_API_KEY, FUB_BASE_URL


def get_person(person_id: str) -> dict | None:
    fub = FUBProcessor(
        api_key=FUB_API_KEY,
        base_url=FUB_BASE_URL
    )
    person = fub.get_person_by_id(person_id)
    logger.info(f"PERSON DATA - {person}")
    if person:
        return schemas.FUBItemResponse(
            data=person
        )
    return schemas.NoFoundResponse()


def get_user(user_id: str) -> dict | None:
    fub = FUBProcessor(
        api_key=FUB_API_KEY,
        base_url=FUB_BASE_URL
    )
    user = fub.get_user_by_id(user_id)
    logger.info(f"USER DATA - {user}")
    return user
