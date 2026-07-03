from pathlib import Path

from app.application.dto.panel import PanelCreateDTO
from app.application.services.panel_service import PanelService
from app.core.config import settings


def test_panel_service_create_and_list(tmp_path: Path) -> None:
    target = tmp_path / "panels.json"
    settings.panel_config_path = str(target)

    service = PanelService()
    created = service.create_panel(
        PanelCreateDTO(
            name="main-hiddify",
            panel_type="hiddify",
            base_url="https://hiddify.example.com",
            api_key="secret-token",
            enabled=True,
            verify_ssl=True,
        )
    )
    assert created.name == "main-hiddify"

    panels = service.list_panels()
    assert len(panels) == 1
    assert panels[0].panel_type == "hiddify"
