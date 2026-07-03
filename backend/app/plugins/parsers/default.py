import base64
import json
from typing import Any

from app.plugins.parsers.base import ParserPlugin


class JsonParser(ParserPlugin):
    name = "json"

    def can_parse(self, payload: str) -> bool:
        candidate = payload.strip()
        return candidate.startswith("{") or candidate.startswith("[")

    def parse(self, payload: str) -> list[dict[str, Any]]:
        data = json.loads(payload)
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            return [data]
        return []


class Base64Parser(ParserPlugin):
    name = "base64"

    def can_parse(self, payload: str) -> bool:
        try:
            base64.b64decode(payload.encode("utf-8"), validate=True)
            return True
        except Exception:
            return False

    def parse(self, payload: str) -> list[dict[str, Any]]:
        decoded = base64.b64decode(payload.encode("utf-8")).decode("utf-8", errors="ignore")
        lines = [line.strip() for line in decoded.splitlines() if line.strip()]
        return [{"uri": line, "source_format": "base64"} for line in lines]


class RawUriParser(ParserPlugin):
    name = "raw_uri"

    def can_parse(self, payload: str) -> bool:
        return any(payload.strip().startswith(prefix) for prefix in ("vless://", "vmess://", "trojan://", "ss://"))

    def parse(self, payload: str) -> list[dict[str, Any]]:
        lines = [line.strip() for line in payload.splitlines() if line.strip()]
        return [{"uri": line, "source_format": "raw"} for line in lines]
