#!/usr/bin/env python3
"""Interactive panel setup for NSM with per-panel API header config."""

from __future__ import annotations

import base64
import hashlib
import json
from getpass import getpass
from pathlib import Path

from cryptography.fernet import Fernet

PANEL_TYPES = ("hiddify", "marzban", "3x-ui", "xray")

PANEL_DEFAULTS = {
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


def _secret_key() -> str:
    env_path = Path("backend/.env")
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("SECRET_KEY="):
                return line.split("=", 1)[1].strip()
    return "change-me-in-production"


def _encrypt(raw: str) -> str:
    digest = hashlib.sha256(_secret_key().encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return "enc:" + Fernet(key).encrypt(raw.encode("utf-8")).decode("utf-8")


def ask_bool(prompt: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    raw = input(f"{prompt} [{suffix}]: ").strip().lower()
    if not raw:
        return default
    return raw in {"y", "yes", "1", "true"}


def ask_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("⚠️ مقدار نمی‌تواند خالی باشد.")


def ask_optional(prompt: str, default: str = "") -> str:
    value = input(f"{prompt} [default: {default or '(empty)'}]: ").strip()
    return value if value else default


def collect_panel(panel_type: str, required: bool = False) -> dict | None:
    if not required:
        enabled = ask_bool(f"آیا پنل {panel_type} را اضافه کنیم؟", default=False)
        if not enabled:
            return None

    defaults = PANEL_DEFAULTS[panel_type]

    print(f"\n--- تنظیم پنل {panel_type} ---")
    name = ask_non_empty("نام دلخواه پنل: ")
    base_url = ask_non_empty("آدرس API پنل (مثال: https://panel.example.com): ")
    api_key = getpass("API Key / Token پنل: ").strip()
    while not api_key:
        print("⚠️ API Key نمی‌تواند خالی باشد.")
        api_key = getpass("API Key / Token پنل: ").strip()

    verify_ssl = ask_bool("بررسی SSL فعال باشد؟", default=True)
    api_header_name = ask_optional("نام هدر API", defaults["api_header_name"])
    api_prefix = ask_optional("پیشوند هدر (مثل Bearer یا خالی)", defaults["api_prefix"])
    proxy_path = ask_optional("proxy_path اگر وجود دارد", defaults["proxy_path"]).strip("/")
    test_endpoint = ask_optional("endpoint برای تست اتصال", defaults["test_endpoint"])

    return {
        "name": name,
        "panel_type": panel_type,
        "base_url": base_url,
        "api_key": _encrypt(api_key),
        "enabled": True,
        "verify_ssl": verify_ssl,
        "api_header_name": api_header_name,
        "api_prefix": api_prefix,
        "proxy_path": proxy_path,
        "test_endpoint": test_endpoint,
    }


def main() -> None:
    print("🚀 NSM Panel Setup Wizard")
    print("API هر پنل (هدر/پیشوند/proxy_path) قابل تنظیم است.\n")

    panels: list[dict] = []

    print("[الزامی] ابتدا Hiddify را وارد کنید:")
    hiddify = collect_panel("hiddify", required=True)
    if hiddify:
        panels.append(hiddify)

    for panel_type in PANEL_TYPES:
        if panel_type == "hiddify":
            continue
        panel = collect_panel(panel_type)
        if panel:
            panels.append(panel)

    output = {"panels": panels}
    config_path = Path("backend/config/panels.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n✅ فایل تنظیمات پنل‌ها ساخته شد:", config_path)
    print("🔐 این فایل شامل API Key رمزنگاری‌شده است؛ commit نکنید.")


if __name__ == "__main__":
    main()
