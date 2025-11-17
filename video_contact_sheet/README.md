# video_contact_sheet

Generate visually rich contact-sheet thumbnails (aka filmstrips) for any number
of videos—handy for quick QA or cataloging.

```bash
# single file
python -m video_contact_sheet.cli demo.mp4 -o out

# entire folder, 8 threads
python -m video_contact_sheet.cli /videos -o out --threads 8 --cols 6
```

## Features
Scene-change detection for “interesting” keyframes
Multithreaded extraction using OpenCV + ffmpeg
Footer shows duration / resolution / codec
Pure-Python, works on Windows/Linux/macOS

