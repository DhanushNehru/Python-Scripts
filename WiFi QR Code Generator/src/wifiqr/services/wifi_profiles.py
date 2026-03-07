"""WLAN profile XML generation for Windows exports."""

from __future__ import annotations

from wifiqr.constants import WINDOWS_SECURITY_DEFAULT, WINDOWS_SECURITY_MAP
from wifiqr.services.wifi_payload import WifiConfig, normalize_security
from wifiqr.services.xml_utils import xml_escape


def _security_to_profile(config: WifiConfig) -> tuple[str, str, str | None]:
    """Map a Wi-Fi config to profile authentication values."""
    security = normalize_security(config.security)
    return WINDOWS_SECURITY_MAP.get(security, WINDOWS_SECURITY_DEFAULT)


def build_wlan_profile_xml(config: WifiConfig) -> str:
    """Build WLAN profile XML content for a Wi-Fi config."""
    auth, encryption, key_type = _security_to_profile(config)
    ssid = xml_escape(config.ssid)
    password = xml_escape(config.password)
    hidden = "true" if config.hidden else "false"

    key_material = (
        f"<sharedKey><keyType>{key_type}</keyType><protected>false</protected>"
        f"<keyMaterial>{password}</keyMaterial></sharedKey>"
        if key_type
        else ""
    )

    return (
        "<?xml version=\"1.0\"?>"
        "<WLANProfile xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v1\">"
        f"<name>{ssid}</name>"
        "<SSIDConfig>"
        "<SSID>"
        f"<name>{ssid}</name>"
        "</SSID>"
        f"<nonBroadcast>{hidden}</nonBroadcast>"
        "</SSIDConfig>"
        "<connectionType>ESS</connectionType>"
        "<connectionMode>auto</connectionMode>"
        "<MSM>"
        "<security>"
        "<authEncryption>"
        f"<authentication>{auth}</authentication>"
        f"<encryption>{encryption}</encryption>"
        "<useOneX>false</useOneX>"
        "</authEncryption>"
        f"{key_material}"
        "</security>"
        "</MSM>"
        "</WLANProfile>"
    )
