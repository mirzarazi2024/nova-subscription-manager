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
