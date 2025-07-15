# Face Blur
```bash
python demo.py
# Choose: 1) Your own image, 2) Webcam capture, or 3) Test pattern
``` Tool 

A powerful yet simple Python tool for automatically detecting and blurring faces in images, videos, and live webcam feeds.

## 🚀 Get Started in 2 Minutes!

### 1. Install 
```bash
pip install -r requirements.txt
```

### 2. Test 
```bash
python demo.py
```

### 3. Use 
```bash
# Blur a photo
python face_blur.py --input your_photo.jpg

# Live webcam blur  
python face_blur.py --input 0 --mode webcam

# Process video
python face_blur.py --input video.mp4 --mode video
```

That's it! 🎉

### More Quick Examples
```bash
# Better quality detection
python face_blur.py --input photo.jpg --method mediapipe

# Pixelate faces for privacy
python face_blur.py --input photo.jpg --blur-type pixelate

# Process entire folder
python face_blur.py --input ./photos --mode batch
```

**Need Help?** Having issues? Try `python demo.py` first!

## Features

- 🔍 **Smart Detection**: Multiple AI methods (Haar Cascades, MediaPipe, DNN)
- 🌊 **Various Blur Effects**: Gaussian, motion blur, and pixelation
- 📸 **Multiple Sources**: Images, videos, webcam, batch processing
- ⚡ **Real-time**: Optimized for live webcam processing
- 🎛️ **Customizable**: Adjustable blur intensity and detection settings
- 🌍 **Cross-platform**: Windows, macOS, Linux

## Usage Examples

### Images
```bash
# Basic image processing
python face_blur.py --input selfie.jpg --mode image

# High quality with MediaPipe
python face_blur.py --input photo.jpg --method mediapipe

# Custom blur effect
python face_blur.py --input photo.jpg --blur-type pixelate --blur-intensity 25
```

### Videos
```bash
# Process video file
python face_blur.py --input family_video.mp4 --mode video

# Custom output location
python face_blur.py --input video.mp4 --mode video --output blurred_video.mp4
```

### Webcam
```bash
# Live webcam blur
python face_blur.py --input 0 --mode webcam

# Save webcam session
python face_blur.py --input 0 --mode webcam --save-webcam
```

### Batch Processing
```bash
# Process all images in folder
python face_blur.py --input ./photos --mode batch --output ./blurred_photos
```

## Options

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `--input` | Input file/directory/camera | Required | File path, directory, or `0` for webcam |
| `--mode` | Processing mode | `image` | `image`, `video`, `webcam`, `batch` |
| `--method` | Detection method | `haar` | `haar`, `mediapipe`, `dnn` |
| `--blur-type` | Blur effect type | `gaussian` | `gaussian`, `motion`, `pixelate` |
| `--blur-intensity` | Blur strength | `21` | Any odd number |
| `--output` | Output location | Auto | File/directory path |

## Detection Methods

- **Haar Cascades** (`haar`) - Fast, lightweight, good for real-time
- **MediaPipe** (`mediapipe`) - Modern AI, very accurate and fast  
- **DNN** (`dnn`) - Deep learning, highest accuracy (requires model download)

## Blur Types

- **Gaussian** - Smooth, natural blur
- **Motion** - Simulates camera movement
- **Pixelate** - Reduces resolution for privacy

## Requirements

- opencv-python>=4.8.0
- numpy>=1.21.0
- mediapipe>=0.10.0
- argparse
- pathlib
- MediaPipe (optional, for better accuracy)
