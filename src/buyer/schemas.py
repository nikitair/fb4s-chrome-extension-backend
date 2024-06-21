from pydantic import BaseModel, Field
from typing import List


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
    sign_rca_form_url: str = 'https://www.findbusinesses4sale.com/'


class BuyerNotFoundResponse(BaseModel):
    error: str = "Buyer NOT Found"


class Lead(BaseModel):
    mls: str
    city: str
    province: str
    postal_code: str
    category: str
    address: str
    price: int
    latitude: float | None
    longitude: float | None


class BuyerLeads(BaseModel):
    leads: List[Lead]


class InPersonEvaluation(BaseModel):
    call_event: str
    evaluator_type: str
    evaluator_name: str
    mark: int
    comment: str | None
    date: str


class BuyerInPersonEvaluations(BaseModel):
    evaluations: List[InPersonEvaluation]


class LeadScoreEvent(BaseModel):
    event: str
    events_amount: int
    event_score: int
    all_events_score: int
    total_score: int


class BuyerLeadScoreEvents(BaseModel):
    events: List[LeadScoreEvent]


class Category(BaseModel):
    category: str
    listings_amount: int
    min_price: int
    avg_price: int
    max_price: int


class BuyerCategories(BaseModel):
    categories: List[Category]


class ViewedListing(BaseModel):
    mls: str
    views_amount: int
    event_date: str
    city: str
    province: str
    category: str
    tags: str
    price: int
    assigned_realtor_name: str
    assigned_realtor_email: str
    assigned_realtor_phone: str
    listing_url: str
    image_url: str


class BuyerViewedListings(BaseModel):
    listings: List[ViewedListing]


class NotViewedListing(BaseModel):
    mls: str
    category: str
    tags: str
    price: str
    city: str
    province: str
    postal_code: str
    listing_url: str
    date_listed: str
    image_url: str


class BuyerNotViewedListings(BaseModel):
    listings: List[NotViewedListing]


class ContactSellerListing(BaseModel):
    mls: str
    views_amount: int
    event_date: str
    city: str
    province: str
    category: str
    tags: str
    price: int
    assigned_realtor_name: str
    assigned_realtor_email: str
    assigned_realtor_phone: str
    listing_url: str
    image_url: str


class BuyerContactSellerListingListings(BaseModel):
    listings: List[ContactSellerListing]


class GreenButtonListing(BaseModel):
    mls: str
    views_amount: int
    event_date: str
    city: str
    province: str
    category: str
    tags: str
    price: int
    assigned_realtor_name: str
    assigned_realtor_email: str
    assigned_realtor_phone: str
    listing_url: str
    image_url: str


class BuyerGreenButtonListings(BaseModel):
    listings: List[GreenButtonListing]
