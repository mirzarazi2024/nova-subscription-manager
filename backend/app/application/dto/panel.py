from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

PanelType = Literal["hiddify", "marzban", "3x-ui", "xray"]


class PanelCreateDTO(BaseModel):
    name: str = Field(min_length=2)
    panel_type: PanelType
    base_url: HttpUrl
    api_key: str = Field(min_length=4)
    enabled: bool = True
    verify_ssl: bool = True
    api_header_name: str | None = None
    api_prefix: str | None = None
    proxy_path: str = ""
    test_endpoint: str | None = None


class PanelUpdateDTO(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    base_url: HttpUrl | None = None
    api_key: str | None = Field(default=None, min_length=4)
    enabled: bool | None = None
    verify_ssl: bool | None = None
    api_header_name: str | None = None
    api_prefix: str | None = None
    proxy_path: str | None = None
    test_endpoint: str | None = None


class PanelReadDTO(BaseModel):
    name: str
    panel_type: PanelType
    base_url: HttpUrl
    api_key_masked: str
    enabled: bool
    verify_ssl: bool
    api_header_name: str
    api_prefix: str
    proxy_path: str
    test_endpoint: str


class PanelConnectionTestDTO(BaseModel):
    panel_type: PanelType
    base_url: HttpUrl
    api_key: str = Field(min_length=4)
    verify_ssl: bool = True
    api_header_name: str | None = None
    api_prefix: str | None = None
    proxy_path: str = ""
    test_endpoint: str | None = None


class PanelConnectionTestResultDTO(BaseModel):
    success: bool
    message: str
    status_code: int | None = None


class PanelAutoDetectRequestDTO(BaseModel):
    panel_type: PanelType
    base_url: HttpUrl
    api_key: str = Field(min_length=4)
    verify_ssl: bool = True
    proxy_path: str = ""


class PanelAutoDetectResponseDTO(BaseModel):
    success: bool
    detected_header_name: str
    detected_prefix: str
    detected_test_endpoint: str | None = None
    working_endpoints: list[str] = Field(default_factory=list)
    message: str
