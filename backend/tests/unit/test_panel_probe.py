import pytest

from app.application.dto.panel import PanelConnectionTestDTO
from app.infrastructure.clients.panel_probe import panel_probe_service


@pytest.mark.asyncio
async def test_probe_returns_result_for_other_panel_types() -> None:
    result = await panel_probe_service.test_connection(
        PanelConnectionTestDTO(
            panel_type="marzban",
            base_url="https://example.com",
            api_key="abcd1234",
            verify_ssl=True,
        )
    )
    assert isinstance(result.success, bool)
    assert isinstance(result.message, str)
