from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.deps import DBSession
from app.application.dto.user import UserReadDTO, UserSyncResultDTO
from app.application.services.user_service import user_service
from app.security.dependencies import CurrentUser, require_roles

router = APIRouter()


@router.get("", response_model=list[UserReadDTO])
async def list_users(
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator", "user"))],
) -> list[UserReadDTO]:
    users = await user_service.list_users(session)
    return [UserReadDTO.model_validate(user) for user in users]


@router.post("/sync", response_model=UserSyncResultDTO)
async def sync_users(
    session: DBSession,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> UserSyncResultDTO:
    return await user_service.sync_hiddify_users(session)
