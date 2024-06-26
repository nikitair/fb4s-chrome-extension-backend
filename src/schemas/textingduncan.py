from pydantic import BaseModel


class FUBNoteCreated(BaseModel):
    eventId: str
    eventCreated: str
    event: str
    resourceIds: list[int]
    uri: str


class SendSMS(BaseModel):
    to_number: str
    sms_body: str


class SendSMSResponse(BaseModel):
    success: bool
    to_phone_number: str | None = None
    sms_message: str | None = None


class NoteProcessing(BaseModel):
    sms_text: str | None = None
    contact_name: str | None = None
    contact_phone: str | None = None
    sms_sent: bool
    assigned_team_member_id: int | None = None
    sms_signature: str | None = None


class FUBNoteCreatedResponse(BaseModel):
    success: bool
    data: NoteProcessing


class MailWizzWebhook(BaseModel):
    campaign_special_id: int
    to_phone_number: str
    campaign_day: int
    jerk_realtor_name: str | None = None
    tm_name: str | None = None
    mls: str | None = None


class MailWizzWebhookResponse(BaseModel):
    success: bool
    sms_template: str | None = None
