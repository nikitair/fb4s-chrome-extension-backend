from pydantic import BaseModel


class GetBuyerProfile(BaseModel):
    access_level_key: str | None = None
    profile_ekey: str | None = None
    profile_ikey: str | None = None
