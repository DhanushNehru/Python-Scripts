"""
Command-line tool: bulk process folders / single files; supports multi-threading.
"""
from __future__ import annotations

import click
from pathlib import Path
from tqdm import tqdm

from .core import video_to_contact_sheet
from .utils import parallel_map

@click.command()
@click.argument("inputs", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--out-dir", type=click.Path(path_type=Path), default="sheets")
@click.option("--max-frames", default=15, show_default=True)
@click.option("--cols", default=5, show_default=True, help="Columns in grid")
@click.option("--scene-thresh", default=30.0, show_default=True, help="Scene-change threshold (higher = fewer frames)")
@click.option("--threads", default=4, show_default=True, help="Parallel workers")
def main(
    inputs: tuple[Path],
    out_dir: Path,
    max_frames: int,
    cols: int,
    scene_thresh: float,
    threads: int,
):
    """Generate contact sheets for videos or folders of videos."""

    vids = []
    for p in inputs:
        if p.is_dir():
            vids.extend(list(p.rglob("*.mp4")))
        else:
            vids.append(p)
    if not vids:
        click.echo("No videos found.", err=True)
        raise SystemExit(1)

    click.echo(f"Processing {len(vids)} video(s)…")
    task = lambda v: video_to_contact_sheet(
        v, out_dir, max_frames=max_frames, cols=cols, scene_thresh=scene_thresh
    )
    for _ in tqdm(parallel_map(task, vids, max_workers=threads), total=len(vids)):
        pass
    click.echo(f"Done! Saved to {out_dir}")


if __name__ == "__main__":
    main()