from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ProviderCreateDTO(BaseModel):
    name: str
    description: str | None = None
    url: HttpUrl
    category: str = "external"
    priority: int = 0
    enabled: bool = True
    cache_duration_seconds: int = 300
    update_interval_seconds: int = 60


class ProviderReadDTO(BaseModel):
    id: str
    name: str
    description: str | None
    url: str
    category: str
    priority: int
    enabled: bool
    status: str
    health_score: float
    scoring_total: float
    last_update_at: datetime | None

    model_config = {"from_attributes": True}
