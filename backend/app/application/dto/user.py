from pydantic import BaseModel


class UserReadDTO(BaseModel):
    id: str
    hiddify_user_id: str
    username: str
    email: str | None
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class UserSyncResultDTO(BaseModel):
    created: int
    updated: int
    disabled: int
    total_remote: int
