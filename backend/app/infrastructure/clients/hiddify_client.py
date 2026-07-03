from typing import Any

import httpx

from app.core.config import settings
from app.core.panels import PanelConfig, build_auth_headers, get_enabled_panels, make_endpoint


class HiddifyClient:
    def _resolve_connection(self) -> PanelConfig:
        for panel in get_enabled_panels():
            if panel.panel_type == "hiddify":
                return panel

        return PanelConfig(
            name="legacy-hiddify",
            panel_type="hiddify",
            base_url=settings.hiddify_api_url,
            api_key=settings.hiddify_api_key,
            enabled=True,
            verify_ssl=True,
            api_header_name="Hiddify-API-Key",
            api_prefix="",
            proxy_path=settings.hiddify_proxy_path,
            test_endpoint="/api/v2/admin/user/",
        )

    async def list_users(self) -> list[dict[str, Any]]:
        panel = self._resolve_connection()
        async with httpx.AsyncClient(base_url=str(panel.base_url), timeout=30, verify=panel.verify_ssl) as client:
            response = await client.get(
                make_endpoint(panel, "/api/v2/admin/user/"),
                headers=build_auth_headers(panel),
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []

    async def get_user_subscription(self, user_uuid: str) -> str:
        panel = self._resolve_connection()
        async with httpx.AsyncClient(base_url=str(panel.base_url), timeout=30, verify=panel.verify_ssl) as client:
            response = await client.get(
                make_endpoint(panel, f"/api/v2/user/{user_uuid}/all-configs/"),
                headers=build_auth_headers(panel),
            )
            response.raise_for_status()
            payload = response.json()
            return str(payload.get("sub_url", ""))


hiddify_client = HiddifyClient()
