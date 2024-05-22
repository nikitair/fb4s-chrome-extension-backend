from pydantic import BaseModel


class DefaultResponse(BaseModel):
    success: bool
    service: str
    router: str
