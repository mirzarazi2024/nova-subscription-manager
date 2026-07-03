from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.v1.deps import DBSession
from app.application.dto.provider import ProviderCreateDTO, ProviderReadDTO
from app.application.services.provider_service import provider_service
from app.db.models import Provider
from app.security.dependencies import CurrentUser, require_roles

router = APIRouter()


@router.get("", response_model=list[ProviderReadDTO])
async def list_providers(
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator", "user"))],
) -> list[ProviderReadDTO]:
    providers = await provider_service.list_providers(session)
    return [ProviderReadDTO.model_validate(provider) for provider in providers]


@router.post("", response_model=ProviderReadDTO, status_code=status.HTTP_201_CREATED)
async def create_provider(
    payload: ProviderCreateDTO,
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> ProviderReadDTO:
    provider = await provider_service.create_provider(session, payload)
    return ProviderReadDTO.model_validate(provider)


@router.post("/{provider_id}/refresh")
async def refresh_provider(
    provider_id: str,
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> dict[str, int]:
    result = await session.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return await provider_service.refresh_provider(session, provider)
