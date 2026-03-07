"""macOS configuration profile generation helpers."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from wifiqr.constants import MACOS_SECURITY_DEFAULT, MACOS_SECURITY_MAP
from wifiqr.services.wifi_payload import WifiConfig, normalize_security
from wifiqr.services.xml_utils import xml_escape


@dataclass(frozen=True)
class MacProfileExport:
    identifier: str
    content: str


def _build_wifi_payload(
    config: WifiConfig,
    payload_identifier: str,
    wifi_uuid: str,
) -> str:
    """Build a Wi-Fi payload dict for a macOS configuration profile."""
    ssid = xml_escape(config.ssid)
    password = xml_escape(config.password)
    hidden = "true" if config.hidden else "false"

    security = normalize_security(config.security)
    encryption = MACOS_SECURITY_MAP.get(security, MACOS_SECURITY_DEFAULT)

    password_block = ""
    if encryption != "None":
        password_block = f"<key>Password</key><string>{password}</string>"

    return (
        "<dict>"
        "<key>PayloadType</key><string>com.apple.wifi.managed</string>"
        "<key>PayloadVersion</key><integer>1</integer>"
        f"<key>PayloadIdentifier</key><string>{payload_identifier}</string>"
        f"<key>PayloadUUID</key><string>{wifi_uuid}</string>"
        f"<key>PayloadDisplayName</key><string>WiFi {ssid}</string>"
        f"<key>SSID_STR</key><string>{ssid}</string>"
        f"<key>HIDDEN_NETWORK</key><{hidden}/>"
        f"<key>EncryptionType</key><string>{encryption}</string>"
        f"{password_block}"
        "</dict>"
    )


def build_macos_mobileconfig(config: WifiConfig) -> MacProfileExport:
    """Build a single-network macOS configuration profile."""
    profile_uuid = str(uuid.uuid4())
    wifi_uuid = str(uuid.uuid4())
    identifier = f"com.wifiqr.profile.{profile_uuid}"

    payload = _build_wifi_payload(
        config,
        payload_identifier=f"{identifier}.wifi",
        wifi_uuid=wifi_uuid,
    )

    content = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" "
        "\"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">"
        "<plist version=\"1.0\">"
        "<dict>"
        "<key>PayloadContent</key>"
        "<array>"
        f"{payload}"
        "</array>"
        "<key>PayloadType</key><string>Configuration</string>"
        "<key>PayloadVersion</key><integer>1</integer>"
        f"<key>PayloadIdentifier</key><string>{identifier}</string>"
        f"<key>PayloadUUID</key><string>{profile_uuid}</string>"
        f"<key>PayloadDisplayName</key><string>WifiQR Wi-Fi</string>"
        "<key>PayloadOrganization</key><string>WifiQR</string>"
        "<key>PayloadRemovalDisallowed</key><false/>"
        "</dict>"
        "</plist>"
    )

    return MacProfileExport(identifier=identifier, content=content)


def build_macos_mobileconfig_multi(configs: list[WifiConfig]) -> MacProfileExport:
    """Build a multi-network macOS configuration profile."""
    if not configs:
        raise ValueError("No networks provided")

    profile_uuid = str(uuid.uuid4())
    identifier = f"com.wifiqr.profile.{profile_uuid}"

    payloads = []
    for config in configs:
        wifi_uuid = str(uuid.uuid4())
        payloads.append(
            _build_wifi_payload(
                config,
                payload_identifier=f"{identifier}.wifi.{wifi_uuid}",
                wifi_uuid=wifi_uuid,
            )
        )

    content = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" "
        "\"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">"
        "<plist version=\"1.0\">"
        "<dict>"
        "<key>PayloadContent</key>"
        "<array>"
        f"{''.join(payloads)}"
        "</array>"
        "<key>PayloadType</key><string>Configuration</string>"
        "<key>PayloadVersion</key><integer>1</integer>"
        f"<key>PayloadIdentifier</key><string>{identifier}</string>"
        f"<key>PayloadUUID</key><string>{profile_uuid}</string>"
        f"<key>PayloadDisplayName</key><string>WifiQR Wi-Fi</string>"
        "<key>PayloadOrganization</key><string>WifiQR</string>"
        "<key>PayloadRemovalDisallowed</key><false/>"
        "</dict>"
        "</plist>"
    )

    return MacProfileExport(identifier=identifier, content=content)
