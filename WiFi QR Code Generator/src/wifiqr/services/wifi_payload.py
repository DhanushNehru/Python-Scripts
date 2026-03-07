"""Wi-Fi payload helpers and configuration model."""

from __future__ import annotations

from dataclasses import dataclass

from wifiqr.constants import SECURITY_ALIASES


@dataclass(frozen=True)
class WifiConfig:
    location: str
    ssid: str
    password: str
    security: str
    hidden: bool = False
    image_data: str | None = None  # base64 encoded image


def _escape(value: str) -> str:
    """Escape payload delimiters for QR-encoded Wi-Fi strings."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
    )


def normalize_security(value: str) -> str:
    """Normalize security labels into canonical forms."""
    key = value.upper().strip()
    return SECURITY_ALIASES.get(key, key)


def security_for_qr(value: str) -> str:
    """Map a security label to a QR-compatible value."""
    normalized = normalize_security(value)
    return "nopass" if normalized == "NOPASS" else normalized


def is_open_security(value: str) -> bool:
    """Return True when the security represents an open network."""
    return normalize_security(value) == "NOPASS"


def build_wifi_payload(config: WifiConfig) -> str:
    """Build a Wi-Fi QR payload string from a configuration."""
    ssid = _escape(config.ssid.strip())
    password = _escape(config.password)
    security = security_for_qr(config.security)
    hidden = "true" if config.hidden else "false"

    if security == "nopass":
        return f"WIFI:T:nopass;S:{ssid};H:{hidden};;"

    return f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"
