from pydantic import BaseModel, Field


class ProfileCompletedLevels(BaseModel):
    intro: bool = False
    complete: bool = False
    supplemental: bool = False
    

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
    buyer_time_zone: int = 0
    lead_score: float = 0.0
    assigned_realtor_name: str | None = None
    assigned_realtor_email: str | None = None
    profile_completed_levels: ProfileCompletedLevels
    show_contacts: bool = True


class BuyerNotFoundResponse(BaseModel):
    error: str = "Buyer NOT Found"
