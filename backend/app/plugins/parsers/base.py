from abc import ABC, abstractmethod
from typing import Any


class ParserPlugin(ABC):
    name: str

    @abstractmethod
    def can_parse(self, payload: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, payload: str) -> list[dict[str, Any]]:
        raise NotImplementedError
