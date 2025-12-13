"""
Shared utilities: ffprobe metadata, parallel helpers, paths.
"""
from __future__ import annotations

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, Iterable, List

FFPROBE_CMD = [
    "ffprobe",
    "-v",
    "error",
    "-print_format",
    "json",
    "-show_format",
    "-show_streams",
]


def ffprobe_metadata(path: Path) -> Dict[str, Any]:
    """Return ffprobe JSON metadata for *path*."""
    proc = subprocess.run(
        FFPROBE_CMD + [str(path)], capture_output=True, text=True, check=True
    )
    return json.loads(proc.stdout)


def parallel_map(func, iterable: Iterable, max_workers: int = 4) -> List:
    """Lightweight ThreadPool map that preserves order."""
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(func, item) for item in iterable]
        return [f.result() for f in futures]