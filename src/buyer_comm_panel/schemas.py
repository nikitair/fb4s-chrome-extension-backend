from pydantic import BaseModel


class SuccessfullyContacted(BaseModel):
    buyer_email: str
    buyer_name: str
    evaluator_name: str
    is_isa: bool
    call_event: str = "Successfully Contacted"
    mark: int
    comment: str
    
    
class CallEventResponse(BaseModel):
    success: bool
    call_event: str
    