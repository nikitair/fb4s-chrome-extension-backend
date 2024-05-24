from pydantic import BaseModel


class FUBNoteCreated(BaseModel):
    eventId: str
    eventCreated: str
    event: str
    resourceIds: list[int]
    uri: str


class SendSMSSchema(BaseModel):
    to_number: str
    sms_body: str


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
