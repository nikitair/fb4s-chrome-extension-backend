from pydantic import BaseModel, Field


class BuyerProfile(BaseModel):
    buyer_customer_id: int
    buyer_email: str
    buyer_phone_number: str
    buyer_first_name: str
    buyer_last_name: str
    viewer_is_admin: bool = Field(False, description="Hide contact information (email, phone_number) if false")


class GetBuyerProfileResponse(BaseModel):
    success: bool = True
    data: BuyerProfile | None = None
    message: str| None = None
