from pydantic import BaseModel, Field


class GetBuyerProfileResponse(BaseModel):
    buyer_customer_id: int
    buyer_email: str
    buyer_phone_number: str
    buyer_first_name: str
    buyer_last_name: str
    show_contacts: bool = Field(True, description="Hide contact information (email, phone_number) if false")

