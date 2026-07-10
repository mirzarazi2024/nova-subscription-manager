from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import DBSession
from app.application.dto.subscription import (
    SubscriptionCreateDTO,
    SubscriptionPreviewRequest,
    SubscriptionPreviewResponse,
    SubscriptionReadDTO,
)
from app.application.services.subscription_service import subscription_service
from app.security.dependencies import CurrentUser, require_roles

router = APIRouter()


@router.get("", response_model=list[SubscriptionReadDTO])
async def list_subscriptions(
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator", "user"))],
) -> list[SubscriptionReadDTO]:
    subscriptions = await subscription_service.list_subscriptions(session)
    return [SubscriptionReadDTO.model_validate(subscription) for subscription in subscriptions]


@router.post("", response_model=SubscriptionReadDTO, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    payload: SubscriptionCreateDTO,
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> SubscriptionReadDTO:
    try:
        subscription = await subscription_service.create_subscription(session, payload)
        return SubscriptionReadDTO.model_validate(subscription)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/preview", response_model=SubscriptionPreviewResponse)
async def preview_subscription(
    payload: SubscriptionPreviewRequest,
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator", "user"))],
) -> SubscriptionPreviewResponse:
    return await subscription_service.preview_subscription(session, payload)
