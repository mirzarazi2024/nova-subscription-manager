import hashlib
from dataclasses import dataclass


@dataclass(slots=True)
class NormalizedNode:
    protocol: str
    server: str
    port: int
    uuid: str | None
    public_key: str | None
    sni: str | None
    transport: str | None
    source: str

    def fingerprint(self) -> str:
        raw = "|".join(
            [
                self.server,
                str(self.port),
                self.uuid or "",
                self.protocol,
                self.public_key or "",
                self.sni or "",
                self.transport or "",
            ]
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class MergeEngine:
    def merge(self, hiddify_nodes: list[NormalizedNode], provider_nodes: list[NormalizedNode]) -> tuple[list[NormalizedNode], int]:
        all_nodes = [*hiddify_nodes, *provider_nodes]
        unique: dict[str, NormalizedNode] = {}
        duplicates = 0
        for node in all_nodes:
            fp = node.fingerprint()
            if fp in unique:
                duplicates += 1
                continue
            unique[fp] = node
        return list(unique.values()), duplicates


merge_engine = MergeEngine()
