from pydantic import BaseModel, Field

{
    "id": 12345,
    "email": "john.johnson@mail.com",
    "phone_number": "123-123-1234",
    "first_name": "John",
    "last_name": "Johnson",
    "city": "Vancouver",
    "province": "British Columbia",
    "fub_stage": "A - Hot",
    "registration_time": "07:00 PM - 20 May 2024",
    "buyer_time_zone": "America/Vancouver",
    "buyer_local_time": "02:30 AM - 31 May 2024",
    "lead_score": 3.5,
    "assigned_realtor_name": "Dave Realtor",
    "assigned_realtor_email": "dave.realtor@fb4s.com",
    "profile_completed_levels": [
        "intro",
        "complete",
        "supplemental"
    ],
    "show_contacts": True
}


class GetBuyerProfileResponse(BaseModel):
    id: int
    email: str
    phone_number: str
    first_name: str
    last_name: str
    city: str | None = None
    province: str | None = None
    fub_stage: str = "Not a FUB Buyer"
    registration_time: str | None = None
    buyer_time_zone: str | None = None
    buyer_local_time: str | None = None
    lead_score: float | None = None
    assigned_realtor_name: str | None = None
    assigned_realtor_email: str | None = None
    profile_completed_levels: list[str] = [
        "intro",
        "complete",
        "supplemental"
    ]
    show_contacts: bool = Field(
        True, description="Hide contact information (email, phone_number) if false")


class BuyerNotFoundResponse(BaseModel):
    error: str = "Buyer NOT Found"
