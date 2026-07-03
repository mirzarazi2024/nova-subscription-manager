from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.panel import (
    PanelAutoDetectRequestDTO,
    PanelAutoDetectResponseDTO,
    PanelConnectionTestDTO,
    PanelConnectionTestResultDTO,
    PanelCreateDTO,
    PanelReadDTO,
    PanelUpdateDTO,
)
from app.application.services.panel_service import panel_service
from app.infrastructure.clients.panel_probe import panel_probe_service
from app.security.dependencies import CurrentUser, require_roles

router = APIRouter()


@router.post("/test-connection", response_model=PanelConnectionTestResultDTO)
async def test_panel_connection(
    payload: PanelConnectionTestDTO,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> PanelConnectionTestResultDTO:
    return await panel_probe_service.test_connection(payload)


@router.post("/auto-detect", response_model=PanelAutoDetectResponseDTO)
async def auto_detect_panel_connection(
    payload: PanelAutoDetectRequestDTO,
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> PanelAutoDetectResponseDTO:
    return await panel_probe_service.auto_detect(payload)


@router.get("", response_model=list[PanelReadDTO])
async def list_panels(
    _: Annotated[CurrentUser, Depends(require_roles("admin", "operator"))],
) -> list[PanelReadDTO]:
    return panel_service.list_panels()


@router.post("", response_model=PanelReadDTO, status_code=status.HTTP_201_CREATED)
async def create_panel(
    payload: PanelCreateDTO,
    _: Annotated[CurrentUser, Depends(require_roles("admin"))],
) -> PanelReadDTO:
    try:
        return panel_service.create_panel(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{panel_name}", response_model=PanelReadDTO)
async def update_panel(
    panel_name: str,
    payload: PanelUpdateDTO,
    _: Annotated[CurrentUser, Depends(require_roles("admin"))],
) -> PanelReadDTO:
    try:
        return panel_service.update_panel(panel_name, payload)
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@router.delete("/{panel_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_panel(
    panel_name: str,
    _: Annotated[CurrentUser, Depends(require_roles("admin"))],
) -> None:
    try:
        panel_service.delete_panel(panel_name)
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
