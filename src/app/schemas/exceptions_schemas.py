from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    success: bool = False
    message: str = "Resource NOT found"


class ServerErrorResponse(BaseModel):
    success: bool = False
    message: str = "Internal Server Error :("
