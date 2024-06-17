from pydantic import BaseModel


class NoFoundResponse(BaseModel):
    success: bool = False
    message: str = "Not found"


class FUBItemResponse(BaseModel):
    success: bool = True
    data: dict


class FUBItemsResponse(BaseModel):
    success: bool = True
    data: list
