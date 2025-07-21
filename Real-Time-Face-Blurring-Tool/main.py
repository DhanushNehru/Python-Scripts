import os
import cv2
import numpy as np
import logging
from pathlib import Path

# Configuration
DEFAULT_BLUR_STRENGTH = 61  # Must be odd
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
OUTPUT_IMAGE_FOLDER = "./output_images/"
OUTPUT_VIDEO_FOLDER = "./output_videos/"
WEBCAM_RESOLUTION = (640, 480)
MODEL_PROTOTXT = "deploy.prototxt.txt"
MODEL_WEIGHTS = "res10_300x300_ssd_iter_140000_fp16.caffemodel"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load DNN model once
def load_face_detection_model():
    """Loads the pre-trained face detection model."""
    try:
        base_dir = Path(__file__).parent
        prototxt_path = str(base_dir / "protocol" / MODEL_PROTOTXT)
        model_path = str(base_dir / "model" / MODEL_WEIGHTS)
        
        if not os.path.exists(prototxt_path):
            raise FileNotFoundError(f"Prototxt file not found at {prototxt_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model weights not found at {model_path}")
            
        return cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise
    
face_net = load_face_detection_model()

def save_video(video, output_path, default_fps=30, default_res=WEBCAM_RESOLUTION):
    """
    Initializes a video writer object to save processed video frames.
    Args:
        video: OpenCV video capture object
        output_path: Path to save the output video
        default_fps: Fallback FPS if not detected
        default_res: Fallback resolution if not detected
        
    Returns:
        cv2.VideoWriter object
    """
    try:
        fps = video.get(cv2.CAP_PROP_FPS) or default_fps
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) or default_res[0]
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) or default_res[1]
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        return cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    except Exception as e:
        logger.error(f"Failed to initialize video writer: {e}")
        raise

def blur_faces(image, confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD, 
              blur_strength=DEFAULT_BLUR_STRENGTH):
    """
    Detects and blurs faces in an image.
    
    Args:
        image: Input image (numpy array)
        confidence_threshold: Minimum confidence for face detection (0-1)
        blur_strength: Kernel size for Gaussian blur (must be odd)
        
    Returns:
        Image with blurred faces (numpy array)
    """
    if image is None:
        raise ValueError("Input image cannot be None")
    
    if blur_strength % 2 == 0:
        blur_strength += 1  # Ensure odd kernel size
        logger.debug(f"Adjusted blur strength to {blur_strength} to make it odd")

    (h, w) = image.shape[:2]
    
    try:
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 
            1.0, 
            (300, 300),
            (104.0, 177.0, 123.0)
        )
        
        face_net.setInput(blob)
        detections = face_net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Ensure coordinates stay within image bounds
                startX, startY = max(0, startX), max(0, startY)
                endX, endY = min(w, endX), min(h, endY)

                # Extract and blur face ROI
                face_roi = image[startY:endY, startX:endX]
                blurred_face = cv2.GaussianBlur(face_roi, (blur_strength, blur_strength), 0)
                image[startY:endY, startX:endX] = blurred_face
                
    except Exception as e:
        logger.error(f"Error during face blurring: {e}")
        raise
        
    return image

def blur_faces_images(image_path):
    """Processes an image file and saves the blurred version."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
            
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image from {image_path}")
            
        blurred_image = blur_faces(image)
        
        os.makedirs(OUTPUT_IMAGE_FOLDER, exist_ok=True)
        output_path = os.path.join(OUTPUT_IMAGE_FOLDER, os.path.basename(image_path))
        
        if not cv2.imwrite(output_path, blurred_image):
            raise IOError(f"Failed to save image to {output_path}")
            
        logger.info(f"Successfully saved blurred image to {output_path}")
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise

def process_video_stream(input_source=None, is_webcam=False):
    """
    Processes either a video file or webcam stream with face blurring.
    
    Args:
        input_source: Path to video file (if not webcam)
        is_webcam: Boolean flag for webcam processing
    """
    try:
        os.makedirs(OUTPUT_VIDEO_FOLDER, exist_ok=True)
        
        if is_webcam:
            video = cv2.VideoCapture(0)
            video.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_RESOLUTION[0])
            video.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_RESOLUTION[1])
            output_path = os.path.join(OUTPUT_VIDEO_FOLDER, "webcam_blurred.mp4")
            logger.info("Starting webcam processing...")
        else:
            if not os.path.exists(input_source):
                raise FileNotFoundError(f"Video file not found at {input_source}")
            video = cv2.VideoCapture(input_source)
            name = os.path.basename(input_source)
            output_path = os.path.join(OUTPUT_VIDEO_FOLDER, f"{os.path.splitext(name)[0]}_blurred.mp4")
            logger.info(f"Processing video file: {input_source}")
        
        out = save_video(video, output_path)
        frame_count = 0
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) if not is_webcam else -1
        
        try:
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                    
                frame_count += 1
                if not is_webcam and frame_count % 10 == 0:
                    logger.info(f"Processing frame {frame_count}/{total_frames}")
                
                blurred_frame = blur_faces(frame)
                cv2.imshow('Blurred Feed', blurred_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("User requested early termination")
                    break
                    
                out.write(blurred_frame)
                
        finally:
            out.release()
            video.release()
            cv2.destroyAllWindows()
            logger.info(f"Successfully saved video to {output_path}")
            
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise

def main():
    """Command line interface for the face blurring application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Face blurring application that processes images, videos, or webcam streams"
    )
    parser.add_argument('--image', help='Path to input image')
    parser.add_argument('--video', help='Path to input video')
    parser.add_argument('--webcam', action='store_true', help='Use webcam')
    
    args = parser.parse_args()
    
    try:
        if args.image:
            blur_faces_images(args.image)
        elif args.video:
            process_video_stream(args.video, is_webcam=False)
        elif args.webcam:
            process_video_stream(is_webcam=True)
        else:
            logger.warning("No input source specified. Use --image, --video, or --webcam")
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())