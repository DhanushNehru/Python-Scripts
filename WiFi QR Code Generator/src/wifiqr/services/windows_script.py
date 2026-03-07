"""Windows script generation for Wi-Fi profiles."""

from __future__ import annotations

import base64
from dataclasses import dataclass

from wifiqr.services.wifi_payload import WifiConfig
from wifiqr.services.wifi_profiles import build_wlan_profile_xml


@dataclass(frozen=True)
class ScriptExport:
    ssid: str
    content: str


def _profile_script_block(profile_path: str, profile_xml: str) -> list[str]:
    """Build script lines for writing and importing a WLAN profile."""
    # Base64 the XML to avoid cmd/PowerShell quoting pitfalls.
    xml_b64 = base64.b64encode(profile_xml.encode("utf-8")).decode("ascii")
    return [
        f"set \"PROFILE_PATH={profile_path}\"",
        "powershell -NoProfile -ExecutionPolicy Bypass -Command "
        f"\"$xml=[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{xml_b64}')); "
        "Set-Content -LiteralPath \\\"%PROFILE_PATH%\\\" -Value $xml -Encoding UTF8\"",
        "netsh wlan add profile filename=\"%PROFILE_PATH%\" user=all",
        "del /f /q \"%PROFILE_PATH%\"",
    ]


def build_windows_connect_script(config: WifiConfig) -> ScriptExport:
    """Build a single-network Windows connect script."""
    ssid = config.ssid
    profile_xml = build_wlan_profile_xml(config)
    lines = ["@echo off", "setlocal EnableExtensions DisableDelayedExpansion"]
    lines.extend(_profile_script_block("%TEMP%\\wifi-profile.xml", profile_xml))
    lines.append(f"netsh wlan connect name=\"{ssid}\"")
    lines.append("endlocal")

    script = "\r\n".join(lines) + "\r\n"
    return ScriptExport(ssid=ssid, content=script)


def build_windows_connect_script_multi(configs: list[WifiConfig]) -> ScriptExport:
    """Build a batch Windows connect script for multiple networks."""
    if not configs:
        raise ValueError("No networks provided")

    lines = ["@echo off", "setlocal EnableExtensions DisableDelayedExpansion"]

    for idx, config in enumerate(configs, start=1):
        profile_xml = build_wlan_profile_xml(config)
        temp_name = f"wifi-profile-{idx}.xml"
        lines.extend(
            _profile_script_block(
                f"%TEMP%\\{temp_name}",
                profile_xml,
            )
        )

    last_ssid = configs[-1].ssid
    lines.append(f"netsh wlan connect name=\"{last_ssid}\"")
    lines.append("endlocal")

    script = "\r\n".join(lines) + "\r\n"
    return ScriptExport(ssid=last_ssid, content=script)
