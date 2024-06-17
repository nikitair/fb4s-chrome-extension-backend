from pydantic import BaseModel


class EBlastForm(BaseModel):
    form_name: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    is_broker: str | None = None
    is_working_with_broker: str | None = None
    cash_available: str | None = None
    time_frame: str | None = None
    is_aware_of_loan: str | None = None
    is_sole_owner: str | None = None
    ever_owned_business: str | None = None
    net_worth: str | None = None
    team_member_email: str | None = None
    
    
class EBlastFormResponse(BaseModel):
    success: bool = True
    fub_buyer: bool
    sent_to_eugene: bool
    buyer_fub_id: int | None = None
    team_member_fub_id: int | None = None
    note_subject: str
    note_body: str
    task: str
    tag: str
    sms_phone_number: str | None = None
    sms_body: str | None = None
    email_receiver: str | None = None
    email_subject: str | None = None
    email_body: str | None = None
    
    
    