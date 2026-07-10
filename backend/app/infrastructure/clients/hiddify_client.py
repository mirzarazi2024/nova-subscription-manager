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
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
            if isinstance(data, dict):
                for key in ("data", "users", "items", "results"):
                    value = data.get(key)
                    if isinstance(value, list):
                        return [item for item in value if isinstance(item, dict)]
            return []

    async def get_user_subscription(self, user_uuid: str) -> str:
        """Return the original Hiddify user subscription/config endpoint URL.

        Hiddify's OpenAPI exposes user-by-secret routes as:
        /{proxy_path}/{secret_uuid}/api/v2/user/all-configs/
        so we build that URL directly. We also probe the endpoint to ensure it exists,
        but keep returning the URL even if the response shape is not a JSON object.
        """
        panel = self._resolve_connection()
        endpoint = f"/{user_uuid}/api/v2/user/all-configs/"
        full_path = make_endpoint(panel, endpoint)
        async with httpx.AsyncClient(base_url=str(panel.base_url), timeout=30, verify=panel.verify_ssl) as client:
            response = await client.get(full_path, headers=build_auth_headers(panel))
            if response.status_code == 404:
                fallback = make_endpoint(panel, "/api/v2/user/all-configs/")
                response = await client.get(fallback, headers=build_auth_headers(panel))
                response.raise_for_status()
                return str(client.base_url).rstrip("/") + fallback
            response.raise_for_status()
            return str(client.base_url).rstrip("/") + full_path


hiddify_client = HiddifyClient()
