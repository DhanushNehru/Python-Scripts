"""
video_contact_sheet
~~~~~~~~~~~~~~~~~~~
Generate key-frame contact sheets (filmstrip grids) from videos.

>>> python -m video_contact_sheet.cli --help
"""

from importlib.metadata import version

__all__ = ("__version__",)
__version__: str = version("video_contact_sheet")