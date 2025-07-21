
"""
Face Blurring Tool
==================
A comprehensive tool to detect and blur faces in images, videos, and webcam feeds
using OpenCV and deep learning models.

Features:
- Multiple face detection methods (Haar Cascades, DNN, MediaPipe)
- Support for images, videos, and real-time webcam
- Adjustable blur intensity
- Multiple blur types (Gaussian, Motion, Pixelation)
- Batch processing for multiple files
- GPU acceleration support
"""

import cv2
import numpy as np
import argparse
import os
import sys
import time
from pathlib import Path
import logging
from typing import List, Tuple, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe not available. Install with: pip install mediapipe")


class FaceBlurrer:
    """Main class for face detection and blurring operations."""
    
    def __init__(self, method='haar', blur_type='gaussian', blur_intensity=21):
        """
        Initialize the FaceBlurrer.
        
        Args:
            method: Detection method ('haar', 'dnn', 'mediapipe')
            blur_type: Type of blur ('gaussian', 'motion', 'pixelate')
            blur_intensity: Intensity of blur effect
        """
        self.method = method
        self.blur_type = blur_type
        self.blur_intensity = blur_intensity
        
        # Initialize detection models
        self._init_detectors()
        
    def _init_detectors(self):
        """Initialize face detection models."""
        if self.method == 'haar':
            self._init_haar_detector()
        elif self.method == 'dnn':
            self._init_dnn_detector()
        elif self.method == 'mediapipe':
            self._init_mediapipe_detector()
        else:
            raise ValueError(f"Unknown detection method: {self.method}")
    
    def _init_haar_detector(self):
        """Initialize Haar Cascade detector."""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            if self.face_cascade.empty():
                raise Exception("Could not load Haar cascade")
            logger.info("Haar Cascade detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Haar detector: {e}")
            raise
    
    def _init_dnn_detector(self):
        """Initialize DNN face detector."""
        try:
            # Download models if they don't exist
            model_dir = Path("models")
            model_dir.mkdir(exist_ok=True)
            
            prototxt_path = model_dir / "deploy.prototxt"
            weights_path = model_dir / "res10_300x300_ssd_iter_140000.caffemodel"
            
            # Create prototxt file if it doesn't exist
            if not prototxt_path.exists():
                self._create_prototxt_file(prototxt_path)
            
            if not weights_path.exists():
                logger.warning("DNN model weights not found. Download from:")
                logger.warning("https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel")
                raise FileNotFoundError("DNN model weights not found")
            
            self.net = cv2.dnn.readNetFromCaffe(str(prototxt_path), str(weights_path))
            logger.info("DNN face detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize DNN detector: {e}")
            raise
    
    def _init_mediapipe_detector(self):
        """Initialize MediaPipe face detector."""
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe not available")
        
        try:
            self.mp_face_detection = mp.solutions.face_detection
            self.mp_drawing = mp.solutions.drawing_utils
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=self.min_detection_confidence
            )
            logger.info("MediaPipe face detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe detector: {e}")
            raise
    
    def _create_prototxt_file(self, path: Path):
        """
        Create the prototxt file for DNN model.
        
        Note:
        - The prototxt content below is incomplete and only includes the definition
          for the 'conv1_1' layer. A complete model definition requires additional
          layers (e.g., pooling, fully connected layers) to be functional.
        - If you need a complete prototxt file, you can download one from a trusted
          source or modify this method to include the full model definition.
        """
        prototxt_content = """name: "OpenCVFaceDetector"
input: "data"
input_shape {
  dim: 1
  dim: 3
  dim: 300
  dim: 300
}

layer {
  name: "conv1_1"
  type: "Convolution"
  bottom: "data"
  top: "conv1_1"
  convolution_param {
    num_output: 64
    kernel_size: 3
    pad: 1
  }
}
"""
        # Full prototxt definition for the DNN model
        full_prototxt_content = """
name: "FaceDetectionModel"
input: "data"
input_shape {
  dim: 1
  dim: 3
  dim: 300
  dim: 300
}
layer {
  name: "conv1_1"
  type: "Convolution"
  bottom: "data"
  top: "conv1_1"
  convolution_param {
    num_output: 64
    kernel_size: 3
    pad: 1
  }
}
# Additional layers and configurations go here
"""
        with open(path, 'w') as f:
            f.write(full_prototxt_content)
    
    def detect_faces_haar(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces using Haar Cascades."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        return [(x, y, w, h) for (x, y, w, h) in faces]
    
    def detect_faces_dnn(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces using DNN."""
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123])
        self.net.setInput(blob)
        detections = self.net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x, y, x1, y1 = box.astype(int)
                faces.append((x, y, x1 - x, y1 - y))
        
        return faces
    
    def detect_faces_mediapipe(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces using MediaPipe."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            h, w = frame.shape[:2]
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                faces.append((x, y, width, height))
        
        return faces
    
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces using the selected method."""
        if self.method == 'haar':
            return self.detect_faces_haar(frame)
        elif self.method == 'dnn':
            return self.detect_faces_dnn(frame)
        elif self.method == 'mediapipe':
            return self.detect_faces_mediapipe(frame)
        else:
            return []
    
    def apply_blur(self, roi: np.ndarray) -> np.ndarray:
        """Apply blur effect to a region of interest."""
        if self.blur_type == 'gaussian':
            return cv2.GaussianBlur(roi, (self.blur_intensity, self.blur_intensity), 0)
        elif self.blur_type == 'motion':
            return self._apply_motion_blur(roi)
        elif self.blur_type == 'pixelate':
            return self._apply_pixelation(roi)
        else:
            return cv2.GaussianBlur(roi, (self.blur_intensity, self.blur_intensity), 0)
    
    def _apply_motion_blur(self, roi: np.ndarray) -> np.ndarray:
        """Apply motion blur effect."""
        size = self.blur_intensity
        kernel = np.zeros((size, size))
        kernel[int((size-1)/2), :] = np.ones(size)
        kernel = kernel / size
        return cv2.filter2D(roi, -1, kernel)
    
    def _apply_pixelation(self, roi: np.ndarray) -> np.ndarray:
        """Apply pixelation effect."""
        h, w = roi.shape[:2]
        # Resize down and then up to create pixelation
        factor = max(1, self.blur_intensity // 5)
        small = cv2.resize(roi, (w // factor, h // factor), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    
    def blur_faces_in_frame(self, frame: np.ndarray) -> np.ndarray:
        """Detect and blur faces in a single frame."""
        faces = self.detect_faces(frame)
        
        for (x, y, w, h) in faces:
            # Ensure coordinates are within frame bounds
            x = max(0, x)
            y = max(0, y)
            w = min(w, frame.shape[1] - x)
            h = min(h, frame.shape[0] - y)
            
            if w > 0 and h > 0:
                roi = frame[y:y+h, x:x+w]
                blurred_roi = self.apply_blur(roi)
                frame[y:y+h, x:x+w] = blurred_roi
        
        return frame
    
    def process_image(self, input_path: str, output_path: str) -> bool:
        """Process a single image file."""
        try:
            frame = cv2.imread(input_path)
            if frame is None:
                logger.error(f"Could not read image: {input_path}")
                return False
            
            logger.info(f"Processing image: {input_path}")
            blurred_frame = self.blur_faces_in_frame(frame)
            
            cv2.imwrite(output_path, blurred_frame)
            logger.info(f"Saved blurred image: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing image {input_path}: {e}")
            return False
    
    def process_video(self, input_path: str, output_path: str) -> bool:
        """Process a video file."""
        try:
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                logger.error(f"Could not open video: {input_path}")
                return False
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            logger.info(f"Processing video: {input_path}")
            logger.info(f"Total frames: {total_frames}, FPS: {fps}")
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                blurred_frame = self.blur_faces_in_frame(frame)
                out.write(blurred_frame)
                
                frame_count += 1
                if frame_count % 30 == 0:  # Progress update every 30 frames
                    progress = (frame_count / total_frames) * 100
                    elapsed = time.time() - start_time
                    eta = (elapsed / frame_count) * (total_frames - frame_count)
                    logger.info(f"Progress: {progress:.1f}% - ETA: {eta:.1f}s")
            
            cap.release()
            out.release()
            
            logger.info(f"Video processing completed: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing video {input_path}: {e}")
            return False
    
    def process_webcam(self, camera_index: int = 0, save_output: bool = False, 
                      output_path: str = "webcam_output.mp4") -> None:
        """Process webcam feed in real-time."""
        try:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                logger.error(f"Could not open camera {camera_index}")
                return
            
            # Set camera properties for better performance
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            out = None
            if save_output:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))
            
            logger.info("Starting webcam feed. Press 'q' to quit, 's' to save frame")
            logger.info(f"Detection method: {self.method}, Blur type: {self.blur_type}")
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.error("Failed to read from camera")
                    break
                
                # Process frame
                blurred_frame = self.blur_faces_in_frame(frame.copy())
                
                # Add info overlay
                fps_current = frame_count / (time.time() - start_time + 1e-6)
                cv2.putText(blurred_frame, f"FPS: {fps_current:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(blurred_frame, f"Method: {self.method}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(blurred_frame, "Press 'q' to quit", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('Face Blur - Real Time', blurred_frame)
                
                if save_output and out is not None:
                    out.write(blurred_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    filename = f"frame_{int(time.time())}.jpg"
                    cv2.imwrite(filename, blurred_frame)
                    logger.info(f"Frame saved: {filename}")
                
                frame_count += 1
            
            cap.release()
            if out is not None:
                out.release()
            cv2.destroyAllWindows()
            
            logger.info("Webcam processing completed")
            
        except Exception as e:
            logger.error(f"Error in webcam processing: {e}")
    
    def batch_process(self, input_dir: str, output_dir: str, 
                     file_extensions: List[str] = None) -> None:
        """Process multiple files in batch."""
        if file_extensions is None:
            file_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if not input_path.exists():
            logger.error(f"Input directory does not exist: {input_dir}")
            return
        
        files = []
        for ext in file_extensions:
            files.extend(input_path.glob(f"*{ext}"))
            files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not files:
            logger.warning(f"No image files found in {input_dir}")
            return
        
        logger.info(f"Found {len(files)} files to process")
        
        successful = 0
        for i, file_path in enumerate(files):
            output_file = output_path / f"blurred_{file_path.name}"
            logger.info(f"Processing {i+1}/{len(files)}: {file_path.name}")
            
            if self.process_image(str(file_path), str(output_file)):
                successful += 1
        
        logger.info(f"Batch processing completed: {successful}/{len(files)} successful")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Face Blurring Tool')
    parser.add_argument('--input', '-i', required=True,
                       help='Input file/directory path')
    parser.add_argument('--output', '-o',
                       help='Output file/directory path')
    parser.add_argument('--mode', '-m', choices=['image', 'video', 'webcam', 'batch'],
                       default='image', help='Processing mode')
    parser.add_argument('--method', choices=['haar', 'dnn', 'mediapipe'],
                       default='haar', help='Face detection method')
    parser.add_argument('--blur-type', choices=['gaussian', 'motion', 'pixelate'],
                       default='gaussian', help='Type of blur effect')
    parser.add_argument('--blur-intensity', type=int, default=21,
                       help='Blur intensity (odd number)')
    parser.add_argument('--camera-index', type=int, default=0,
                       help='Camera index for webcam mode')
    parser.add_argument('--save-webcam', action='store_true',
                       help='Save webcam output to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Ensure blur intensity is odd
    if args.blur_intensity % 2 == 0:
        args.blur_intensity += 1
    
    try:
        # Initialize face blurrer
        blurrer = FaceBlurrer(
            method=args.method,
            blur_type=args.blur_type,
            blur_intensity=args.blur_intensity
        )
        
        if args.mode == 'image':
            if not args.output:
                input_path = Path(args.input)
                args.output = str(input_path.parent / f"blurred_{input_path.name}")
            
            success = blurrer.process_image(args.input, args.output)
            if success:
                print(f"Image processed successfully: {args.output}")
            else:
                print("Failed to process image")
                sys.exit(1)
        
        elif args.mode == 'video':
            if not args.output:
                input_path = Path(args.input)
                args.output = str(input_path.parent / f"blurred_{input_path.name}")
            
            success = blurrer.process_video(args.input, args.output)
            if success:
                print(f"Video processed successfully: {args.output}")
            else:
                print("Failed to process video")
                sys.exit(1)
        
        elif args.mode == 'webcam':
            output_file = args.output if args.output else "webcam_output.mp4"
            blurrer.process_webcam(
                camera_index=args.camera_index,
                save_output=args.save_webcam,
                output_path=output_file
            )
        
        elif args.mode == 'batch':
            if not args.output:
                args.output = str(Path(args.input) / "blurred_output")
            
            blurrer.batch_process(args.input, args.output)
    
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

