"""
Core logic: Keyframe extraction, contact table splicing.
"""
from __future__ import annotations

import math
import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple

from .utils import ffprobe_metadata


def extract_keyframes(
    video_path: Path, max_frames: int = 15, scene_thresh: float = 30.0
) -> List[np.ndarray]:
    """
    Return up to *max_frames* key frames (BGR ndarray). 
    Use HSV histogram difference for simple scene change detection.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open {video_path}")

    frames: List[np.ndarray] = []
    prev_hist = None

    while len(frames) < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        if prev_hist is None:
            frames.append(frame)
        else:
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
            if diff * 100 > scene_thresh:  # scale for intuition
                frames.append(frame)
        prev_hist = hist

    cap.release()
    if not frames:
        raise RuntimeError("No frames extracted")
    return frames


FONT = ImageFont.load_default()


def make_contact_sheet(
    frames: List[np.ndarray],
    metadata: Dict,
    cols: int = 5,
    margin: int = 8,
) -> Image.Image:

    rows = math.ceil(len(frames) / cols)
    h, w, _ = frames[0].shape
    sheet_w = w * cols + margin * (cols + 1)
    sheet_h = h * rows + margin * (rows + 1) + 60 
    canvas = Image.new("RGB", (sheet_w, sheet_h), "black")

    for idx, frame in enumerate(frames):
        r = idx // cols
        c = idx % cols
        x = margin + c * (w + margin)
        y = margin + r * (h + margin)
        canvas.paste(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), (x, y))

    draw = ImageDraw.Draw(canvas)
    text = (
        f"{metadata['file']}  |  {metadata['duration']:.1f}s  "
        f"|  {metadata['width']}x{metadata['height']}  |  {metadata['codec']}"
    )
    tw, th = draw.textsize(text, font=FONT)
    draw.text(((sheet_w - tw) // 2, sheet_h - th - 10), text, fill="white", font=FONT)
    return canvas


def video_to_contact_sheet(
    video_path: Path,
    out_dir: Path,
    max_frames: int = 15,
    cols: int = 5,
    scene_thresh: float = 30.0,
    quality: int = 85,
) -> Path:

    frames = extract_keyframes(video_path, max_frames=max_frames, scene_thresh=scene_thresh)
    meta = _collect_meta(video_path)
    sheet = make_contact_sheet(frames, meta, cols=cols)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{video_path.stem}_sheet.jpg"
    sheet.save(out_path, "JPEG", quality=quality)
    return out_path


def _collect_meta(video_path: Path) -> Dict:
    info = ffprobe_metadata(video_path)
    v_stream = next(s for s in info["streams"] if s["codec_type"] == "video")
    return dict(
        file=video_path.name,
        duration=float(info["format"]["duration"]),
        width=int(v_stream["width"]),
        height=int(v_stream["height"]),
        codec=v_stream["codec_name"],
    )