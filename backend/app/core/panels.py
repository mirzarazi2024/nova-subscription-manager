import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from app.core.config import settings
from app.core.crypto import decrypt_secret, encrypt_secret

PanelType = Literal["hiddify", "marzban", "3x-ui", "xray"]

PANEL_DEFAULTS: dict[PanelType, dict[str, str]] = {
    "hiddify": {
        "api_header_name": "Hiddify-API-Key",
        "api_prefix": "",
        "proxy_path": "",
        "test_endpoint": "/api/v2/admin/user/",
    },
    "marzban": {
        "api_header_name": "Authorization",
        "api_prefix": "Bearer",
        "proxy_path": "",
        "test_endpoint": "/api/system",
    },
    "3x-ui": {
        "api_header_name": "Authorization",
        "api_prefix": "Bearer",
        "proxy_path": "",
        "test_endpoint": "/panel/api/inbounds/list",
    },
    "xray": {
        "api_header_name": "Authorization",
        "api_prefix": "Bearer",
        "proxy_path": "",
        "test_endpoint": "/api/health",
    },
}


class PanelConfig(BaseModel):
    name: str = Field(min_length=2)
    panel_type: PanelType
    base_url: HttpUrl
    api_key: str = Field(min_length=4)
    enabled: bool = True
    verify_ssl: bool = True
    api_header_name: str = "Authorization"
    api_prefix: str = "Bearer"
    proxy_path: str = ""
    test_endpoint: str = "/"


class PanelSettings(BaseModel):
    panels: list[PanelConfig] = Field(default_factory=list)


def _resolve_path() -> Path:
    configured = Path(settings.panel_config_path)
    if configured.is_absolute():
        return configured

    root = Path(__file__).resolve().parents[2]
    return root / configured


def get_panel_defaults(panel_type: PanelType) -> dict[str, str]:
    return PANEL_DEFAULTS[panel_type].copy()


def build_auth_headers(panel: PanelConfig) -> dict[str, str]:
    token = panel.api_key
    prefix = panel.api_prefix.strip()
    value = f"{prefix} {token}".strip() if prefix else token
    return {panel.api_header_name: value}


def make_endpoint(panel: PanelConfig, endpoint: str) -> str:
    clean_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    proxy_path = panel.proxy_path.strip("/")
    if proxy_path:
        return f"/{proxy_path}{clean_endpoint}"
    return clean_endpoint


def load_panel_settings() -> PanelSettings:
    path = _resolve_path()
    if not path.exists():
        return PanelSettings()

    payload = json.loads(path.read_text(encoding="utf-8"))
    data = PanelSettings.model_validate(payload)

    decrypted: list[PanelConfig] = []
    for panel in data.panels:
        defaults = get_panel_defaults(panel.panel_type)
        panel = panel.model_copy(
            update={
                "api_header_name": panel.api_header_name or defaults["api_header_name"],
                "api_prefix": panel.api_prefix if panel.api_prefix is not None else defaults["api_prefix"],
                "proxy_path": panel.proxy_path,
                "test_endpoint": panel.test_endpoint or defaults["test_endpoint"],
            }
        )
        if panel.api_key.startswith("enc:"):
            key = decrypt_secret(panel.api_key.removeprefix("enc:"))
            decrypted.append(panel.model_copy(update={"api_key": key}))
        else:
            decrypted.append(panel)

    return PanelSettings(panels=decrypted)


def save_panel_settings(data: PanelSettings) -> None:
    path = _resolve_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    encrypted_panels: list[PanelConfig] = []
    for panel in data.panels:
        if panel.api_key.startswith("enc:"):
            encrypted_panels.append(panel)
            continue
        encrypted_panels.append(panel.model_copy(update={"api_key": f"enc:{encrypt_secret(panel.api_key)}"}))

    serialized = PanelSettings(panels=encrypted_panels).model_dump_json(indent=2)
    path.write_text(serialized, encoding="utf-8")


def get_enabled_panels() -> list[PanelConfig]:
    return [panel for panel in load_panel_settings().panels if panel.enabled]
