from pydantic import BaseModel


class Base64Response(BaseModel):
    success: bool = True
    mode: str
    data: str | None
