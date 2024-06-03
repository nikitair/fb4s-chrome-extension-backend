from pydantic import BaseModel, Field


class ProfileCompletedLevels(BaseModel):
    intro: bool = False
    complete: bool = False
    supplemental: bool = False
    

class BuyerProfileResponse(BaseModel):
    id: int | None = None
    email: str | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    province: str | None = None
    fub_stage: str = "Not a FUB Buyer"
    registration_time: str | None = None
    buyer_time_zone: int | None = None
    lead_score: float = 0
    assigned_realtor_name: str | None = None
    assigned_realtor_email: str | None = None
    profile_completed_levels: ProfileCompletedLevels
    show_contacts: bool = True


class BuyerNotFoundResponse(BaseModel):
    error: str = "Buyer NOT Found"
