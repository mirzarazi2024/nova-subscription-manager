import httpx

from app.application.dto.panel import (
    PanelAutoDetectRequestDTO,
    PanelAutoDetectResponseDTO,
    PanelConnectionTestDTO,
    PanelConnectionTestResultDTO,
)
from app.core.panels import PanelConfig, build_auth_headers, get_panel_defaults, make_endpoint


class PanelProbeService:
    async def test_connection(self, payload: PanelConnectionTestDTO) -> PanelConnectionTestResultDTO:
        defaults = get_panel_defaults(payload.panel_type)
        panel = PanelConfig(
            name="probe",
            panel_type=payload.panel_type,
            base_url=payload.base_url,
            api_key=payload.api_key,
            enabled=True,
            verify_ssl=payload.verify_ssl,
            api_header_name=payload.api_header_name or defaults["api_header_name"],
            api_prefix=payload.api_prefix if payload.api_prefix is not None else defaults["api_prefix"],
            proxy_path=payload.proxy_path.strip("/"),
            test_endpoint=payload.test_endpoint or defaults["test_endpoint"],
        )

        async with httpx.AsyncClient(base_url=str(panel.base_url), timeout=20, verify=panel.verify_ssl) as client:
            try:
                endpoint = make_endpoint(panel, panel.test_endpoint)
                response = await client.get(endpoint, headers=build_auth_headers(panel))
                if response.status_code < 300:
                    return PanelConnectionTestResultDTO(
                        success=True,
                        message=f"Connected successfully to {panel.panel_type} ({endpoint})",
                        status_code=response.status_code,
                    )
                return PanelConnectionTestResultDTO(
                    success=False,
                    message=(
                        f"Connection failed for {panel.panel_type}. HTTP {response.status_code}. "
                        f"Check header/prefix/proxy_path/token permissions."
                    ),
                    status_code=response.status_code,
                )
            except httpx.HTTPError as exc:
                return PanelConnectionTestResultDTO(
                    success=False,
                    message=f"Network/HTTP error: {exc}",
                    status_code=None,
                )

    async def auto_detect(self, payload: PanelAutoDetectRequestDTO) -> PanelAutoDetectResponseDTO:
        defaults = get_panel_defaults(payload.panel_type)
        proxy_path = payload.proxy_path.strip("/")

        # For now, strongest autodetect profile is for Hiddify based on uploaded OpenAPI/screenshots
        candidates: list[tuple[str, str, list[str]]] = []
        if payload.panel_type == "hiddify":
            candidates = [
                (
                    "Hiddify-API-Key",
                    "",
                    [
                        "/api/v2/admin/user/",
                        "/api/v2/panel/info/",
                        "/api/v2/panel/ping/",
                    ],
                ),
                ("Authorization", "Bearer", ["/api/v2/admin/user/"]),
            ]
        else:
            candidates = [
                (
                    defaults["api_header_name"],
                    defaults["api_prefix"],
                    [defaults["test_endpoint"]],
                )
            ]

        working_endpoints: list[str] = []
        for header_name, prefix, endpoints in candidates:
            panel = PanelConfig(
                name="autodetect",
                panel_type=payload.panel_type,
                base_url=payload.base_url,
                api_key=payload.api_key,
                enabled=True,
                verify_ssl=payload.verify_ssl,
                api_header_name=header_name,
                api_prefix=prefix,
                proxy_path=proxy_path,
                test_endpoint=endpoints[0],
            )

            async with httpx.AsyncClient(base_url=str(panel.base_url), timeout=20, verify=panel.verify_ssl) as client:
                ok = False
                for endpoint in endpoints:
                    try:
                        full_path = make_endpoint(panel, endpoint)
                        response = await client.get(full_path, headers=build_auth_headers(panel))
                        if response.status_code < 300:
                            working_endpoints.append(endpoint)
                            ok = True
                    except httpx.HTTPError:
                        continue

                if ok:
                    return PanelAutoDetectResponseDTO(
                        success=True,
                        detected_header_name=header_name,
                        detected_prefix=prefix,
                        detected_test_endpoint=working_endpoints[0] if working_endpoints else None,
                        working_endpoints=working_endpoints,
                        message=f"Auto-detect success for {payload.panel_type}",
                    )

        return PanelAutoDetectResponseDTO(
            success=False,
            detected_header_name=defaults["api_header_name"],
            detected_prefix=defaults["api_prefix"],
            detected_test_endpoint=None,
            working_endpoints=[],
            message=(
                "Auto-detect failed. Check base_url, proxy_path, API key and network access. "
                "For Hiddify usually header is Hiddify-API-Key."
            ),
        )


panel_probe_service = PanelProbeService()
