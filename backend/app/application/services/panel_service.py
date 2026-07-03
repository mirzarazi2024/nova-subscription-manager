from app.application.dto.panel import PanelCreateDTO, PanelReadDTO, PanelUpdateDTO
from app.core.panels import (
    PanelConfig,
    PanelSettings,
    get_panel_defaults,
    load_panel_settings,
    save_panel_settings,
)


class PanelService:
    def list_panels(self) -> list[PanelReadDTO]:
        data = load_panel_settings()
        return [self._to_read_dto(panel) for panel in data.panels]

    def create_panel(self, payload: PanelCreateDTO) -> PanelReadDTO:
        data = load_panel_settings()
        for panel in data.panels:
            if panel.name.lower() == payload.name.lower():
                raise ValueError("Panel name already exists")

        defaults = get_panel_defaults(payload.panel_type)
        panel = PanelConfig(
            name=payload.name,
            panel_type=payload.panel_type,
            base_url=payload.base_url,
            api_key=payload.api_key,
            enabled=payload.enabled,
            verify_ssl=payload.verify_ssl,
            api_header_name=payload.api_header_name or defaults["api_header_name"],
            api_prefix=(payload.api_prefix if payload.api_prefix is not None else defaults["api_prefix"]),
            proxy_path=payload.proxy_path.strip("/"),
            test_endpoint=payload.test_endpoint or defaults["test_endpoint"],
        )
        data.panels.append(panel)
        save_panel_settings(data)
        return self._to_read_dto(panel)

    def update_panel(self, panel_name: str, payload: PanelUpdateDTO) -> PanelReadDTO:
        data = load_panel_settings()
        target_idx = next((i for i, p in enumerate(data.panels) if p.name == panel_name), None)
        if target_idx is None:
            raise ValueError("Panel not found")

        current = data.panels[target_idx]
        updates = payload.model_dump(exclude_unset=True)
        if "proxy_path" in updates and updates["proxy_path"] is not None:
            updates["proxy_path"] = updates["proxy_path"].strip("/")

        updated = current.model_copy(update=updates)
        data.panels[target_idx] = updated
        save_panel_settings(data)
        return self._to_read_dto(updated)

    def delete_panel(self, panel_name: str) -> None:
        data = load_panel_settings()
        filtered = [panel for panel in data.panels if panel.name != panel_name]
        if len(filtered) == len(data.panels):
            raise ValueError("Panel not found")

        if not any(panel.panel_type == "hiddify" for panel in filtered):
            raise ValueError("At least one Hiddify panel must remain configured")

        save_panel_settings(PanelSettings(panels=filtered))

    def _to_read_dto(self, panel: PanelConfig) -> PanelReadDTO:
        return PanelReadDTO(
            name=panel.name,
            panel_type=panel.panel_type,
            base_url=panel.base_url,
            api_key_masked=self._mask_api_key(panel.api_key),
            enabled=panel.enabled,
            verify_ssl=panel.verify_ssl,
            api_header_name=panel.api_header_name,
            api_prefix=panel.api_prefix,
            proxy_path=panel.proxy_path,
            test_endpoint=panel.test_endpoint,
        )

    @staticmethod
    def _mask_api_key(secret: str) -> str:
        cleaned = secret[4:] if secret.startswith("enc:") else secret
        if len(cleaned) <= 6:
            return "***"
        return f"{cleaned[:3]}***{cleaned[-3:]}"


panel_service = PanelService()
