# Video Contact Sheet Generator

Automatically generates contact sheet thumbnails for videos by extracting scene-representative frames using HSV histogram difference detection.

## Features

- **Scene-change detection**: Uses HSV histogram difference to identify distinct scenes
- **Multithreaded processing**: Configurable thread count for faster processing
- **Customizable output**: Adjustable grid layout, frame count, and scene detection sensitivity
- **Metadata overlay**: Includes video duration, resolution, and codec information
- **High-quality output**: JPEG contact sheets with optimized quality

## Requirements

- Python 3.6+
- OpenCV (cv2)
- NumPy
- Pillow (PIL)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic usage
```bash
python video_contact_sheet.py input_video.mp4
```

### Advanced usage
```bash
python video_contact_sheet.py input_video.mp4 \
    --output my_contact_sheet.jpg \
    --max-frames 20 \
    --cols 5 \
    --scene-thresh 0.4 \
    --threads 8
```

## Command Line Options

- `video`: Path to input video file (required)
- `-o, --output`: Output contact sheet path (default: auto-generated)
- `--max-frames`: Maximum number of frames to extract (default: 16)
- `--cols`: Number of columns in contact sheet grid (default: 4)
- `--scene-thresh`: Scene change detection threshold 0.0-1.0 (default: 0.3)
  - Lower values = more sensitive to scene changes
  - Higher values = less sensitive to scene changes
- `--threads`: Number of processing threads (default: 4)

## How It Works

1. **Scene Detection**: The tool analyzes video frames using HSV color space histograms
2. **Frame Selection**: Frames with significant histogram differences are selected as scene representatives
3. **Thumbnail Generation**: Selected frames are resized to uniform thumbnails
4. **Grid Layout**: Thumbnails are arranged in a configurable grid
5. **Metadata Footer**: Video information is added to the bottom of the contact sheet

## Output

The generated contact sheet includes:
- Grid of scene-representative thumbnails
- Video metadata footer showing:
  - Duration
  - Resolution
  - Codec information

## Performance

- Processes ~8× realtime on 8-core CPU
- Automatically skips frames for efficiency on long videos
- Memory usage scales with max_frames setting

## Use Cases

- Fast visual QA for large video datasets
- Course content review and cataloging
- Surveillance footage summarization
- Video collection organization
- Content moderation workflows

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

The tests include auto-generated sample videos to ensure functionality works correctly.