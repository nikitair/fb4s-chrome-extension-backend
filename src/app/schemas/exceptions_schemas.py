from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    success: bool = False
    message: str = "Resource NOT found"
