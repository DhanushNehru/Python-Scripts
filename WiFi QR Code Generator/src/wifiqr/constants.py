"""Application-wide constants."""

from __future__ import annotations

# QR Code Generation Defaults
DEFAULT_QR_SIZE = 640
DEFAULT_QR_BOX_SIZE = 10
DEFAULT_QR_BORDER = 2
DEFAULT_QR_FILL_COLOR = "#111827"
DEFAULT_QR_BACKGROUND_COLOR = "white"

# Security Options
SECURITY_OPTIONS = ("WPA/WPA2/WPA3", "WEP", "None")

# Security Label Normalization
SECURITY_ALIASES = {
    "WPA/WPA2/WPA3": "WPA",
    "WPA2": "WPA",
    "WPA3": "WPA",
    "OPEN": "NOPASS",
    "NONE": "NOPASS",
    "NO PASSWORD": "NOPASS",
}

# Windows Profile Security Mapping (auth, encryption, key_type)
WINDOWS_SECURITY_MAP = {
    "NOPASS": ("open", "none", None),
    "WEP": ("open", "WEP", "networkKey"),
}
WINDOWS_SECURITY_DEFAULT = ("WPA2PSK", "AES", "passPhrase")

# macOS Profile Security Mapping
MACOS_SECURITY_MAP = {
    "NOPASS": "None",
    "WEP": "WEP",
}
MACOS_SECURITY_DEFAULT = "WPA"
# UI Performance
PREVIEW_RESIZE_THRESHOLD = 10  # Minimum pixel difference to trigger rescale
