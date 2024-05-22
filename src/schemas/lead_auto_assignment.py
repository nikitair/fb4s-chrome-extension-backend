from pydantic import BaseModel


class LASDetailedInfo(BaseModel):
    win_type: str | None = None
    realtor_category: str | None = None
    buyer_nationality: str | None = None
    realtor_priority: int | None = None


class LASResponse(BaseModel):
    assigned_realtor: str = "willow@fb4s.com"
    possible_realtors: list = []
    realtor_type_1: int = 1
    assigned_pond_id: int = 0
    detailed_info: LASDetailedInfo


class LASRequest(BaseModel):
    postalcode: str = ""
    listing_province: str = ""
    listing_city: str = ""
    listing_categories: str = ""
    listing_mls: str = ""

    buyer_name: str = ""
    buyer_email: str = ""
    buyer_city: str = ""
    buyer_province: str = ""

    cold_lead: str = ""
