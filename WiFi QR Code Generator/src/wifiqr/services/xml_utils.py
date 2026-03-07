"""Shared XML escaping utilities."""

from __future__ import annotations


def xml_escape(value: str) -> str:
    """Escape XML special characters for use in XML/plist content."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
