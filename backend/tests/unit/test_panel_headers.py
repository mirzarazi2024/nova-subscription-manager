from app.core.panels import PanelConfig, build_auth_headers, make_endpoint


def test_hiddify_header_and_proxy_path() -> None:
    panel = PanelConfig(
        name="hiddify-main",
        panel_type="hiddify",
        base_url="https://h.example.com",
        api_key="token123",
        enabled=True,
        verify_ssl=True,
        api_header_name="Hiddify-API-Key",
        api_prefix="",
        proxy_path="admin",
        test_endpoint="/api/v2/admin/user/",
    )

    headers = build_auth_headers(panel)
    assert headers == {"Hiddify-API-Key": "token123"}
    assert make_endpoint(panel, "/api/v2/admin/user/") == "/admin/api/v2/admin/user/"


def test_bearer_header() -> None:
    panel = PanelConfig(
        name="marzban-main",
        panel_type="marzban",
        base_url="https://m.example.com",
        api_key="abcd",
        enabled=True,
        verify_ssl=True,
        api_header_name="Authorization",
        api_prefix="Bearer",
        proxy_path="",
        test_endpoint="/api/system",
    )

    headers = build_auth_headers(panel)
    assert headers == {"Authorization": "Bearer abcd"}
