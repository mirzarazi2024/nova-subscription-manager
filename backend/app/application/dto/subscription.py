from pydantic import BaseModel


class SubscriptionPreviewRequest(BaseModel):
    user_id: str
    provider_ids: list[str]


class SubscriptionPreviewResponse(BaseModel):
    hiddify_nodes: int
    provider_nodes: dict[str, int]
    duplicates_removed: int
    rules_removed: int
    final_nodes: int


class SubscriptionCreateDTO(BaseModel):
    user_id: str
    format: str = "base64"


class SubscriptionReadDTO(BaseModel):
    id: str
    user_id: str
    uuid: str
    source_hiddify_url: str | None
    nova_url: str
    format: str
    is_active: bool
    preview_summary: dict

    model_config = {"from_attributes": True}
