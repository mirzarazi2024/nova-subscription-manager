from app.plugins.parsers.base import ParserPlugin
from app.plugins.parsers.default import Base64Parser, JsonParser, RawUriParser


class ParserRegistry:
    def __init__(self) -> None:
        self._plugins: list[ParserPlugin] = []
        self.register(Base64Parser())
        self.register(JsonParser())
        self.register(RawUriParser())

    def register(self, plugin: ParserPlugin) -> None:
        self._plugins.append(plugin)

    def detect_and_parse(self, payload: str) -> list[dict]:
        for plugin in self._plugins:
            if plugin.can_parse(payload):
                return plugin.parse(payload)
        return []


parser_registry = ParserRegistry()
