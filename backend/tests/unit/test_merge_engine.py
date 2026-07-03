from app.domain.services.merge_engine import NormalizedNode, merge_engine


def test_merge_engine_removes_duplicates() -> None:
    base = NormalizedNode(
        protocol="vless",
        server="a.example.com",
        port=443,
        uuid="u1",
        public_key="pk",
        sni="a.example.com",
        transport="tcp",
        source="hiddify",
    )
    duplicate = NormalizedNode(
        protocol="vless",
        server="a.example.com",
        port=443,
        uuid="u1",
        public_key="pk",
        sni="a.example.com",
        transport="tcp",
        source="provider",
    )
    merged, duplicates = merge_engine.merge([base], [duplicate])
    assert len(merged) == 1
    assert duplicates == 1
