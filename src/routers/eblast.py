from fastapi import APIRouter
from config.logging_config import logger
from schemas.index import DefaultResponse
from schemas import eblast as schemas


eblast_router = APIRouter()


@eblast_router.get('/')
async def eblast_index() -> DefaultResponse:
    return DefaultResponse(
        success=True,
        service="fb4s-automations",
        router="eblast"
    )
    

@eblast_router.post(
    path='/submit',
    responses={
        200: schemas.EBlastFormResponse
    }
)
async def eblast_submit(request: schemas.EBlastForm):
    logger.info("*** E-Blast SUBMISSION TRIGGERED")
    return {
        "message": "Under Development"
    }
