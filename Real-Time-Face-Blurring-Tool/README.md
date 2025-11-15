# Real-Time Face Blurring Tool

A robust Python application for anonymizing faces in images, videos, and live webcam feeds using OpenCV's deep neural network (DNN) module.

## Features

- **Multi-source processing**:
  - 📷 Single image processing
  - 🎥 Video file processing
  - 🌐 Live webcam feed processing
- **Advanced face detection** using Caffe-based DNN model
- **Adjustable parameters**:
  - Blur strength (kernel size)
  - Detection confidence threshold
- **Automatic output organization**:
  - `./output_images/` for processed images
  - `./output_videos/` for processed videos
- **Progress tracking** for video processing
- **Graceful resource handling** with proper cleanup

## Requirements

- Python 3.6+
- Required packages:
  ```bash
  pip install opencv-python numpy
  ```

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/Real-Time-Face-Blurring-Tool.git
cd Real-Time-Face-Blurring-Tool
pip install -r requirements.txt
```

## Model Files

Download the following files and place them in the correct folders:

- `deploy.prototxt.txt` → `protocol/` folder
- `res10_300x300_ssd_iter_140000_fp16.caffemodel` → `model/` folder

You can download them from [OpenCV's GitHub repository](https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector).

## Usage

Process an image:

```bash
python main.py --image path/to/image.jpg
```

Process a video:

```bash
python main.py --video path/to/video.mp4
```

Process webcam feed:

```bash
python main.py --webcam
```

### Optional Arguments

- `--blur` Blur kernel size (odd integer, default: 61)
- `--confidence` Face detection confidence threshold (default: 0.5)

## Output

- Processed images are saved in `./output_images/` with `_blurred` appended to the filename.
- Processed videos are saved in `./output_videos/` with `_blurred` appended to the filename.

## Troubleshooting

- **Model file not found:** Make sure you downloaded the model files and placed them in the correct folders.
- **Webcam not detected:** Ensure your webcam is connected and not used by another application.
- **Permission errors:** Run your terminal or IDE as administrator if you encounter permission issues writing output files.
