from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.deps import DBSession
from app.application.dto.subscription import SubscriptionPreviewRequest, SubscriptionPreviewResponse
from app.application.services.subscription_service import subscription_service
from app.security.dependencies import CurrentUser, require_roles

router = APIRouter()


@router.post("/preview", response_model=SubscriptionPreviewResponse)
async def preview_subscription(
    payload: SubscriptionPreviewRequest,
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator", "user"))],
) -> SubscriptionPreviewResponse:
    return await subscription_service.preview_subscription(session, payload)
