from pydantic import BaseModel


class BaseCustomExceptionSchema(BaseModel):
    success: bool = False
    message: str = "Default HTTP Exception"


class NotFoundResponse(BaseCustomExceptionSchema):
    message: str = "Resource NOT found :("


class ServerErrorResponse(BaseCustomExceptionSchema):
    message: str = "Internal Server Error :("


class NotAuthResponse(BaseCustomExceptionSchema):
    message: str = "You are NOT Authenticated"


class ForbiddenResponse(BaseCustomExceptionSchema):
    message: str = "You are NOT Authorized"


class BadRequestResponse(BaseCustomExceptionSchema):
    message: str = "Bad Request"


class BadPayloadResponse(BaseCustomExceptionSchema):
    message: str = "Bad Request"