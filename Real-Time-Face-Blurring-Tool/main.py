import os
import cv2
import numpy as np

# Load DNN model once to avoid reloading it for each frame
def load_face_detection_model():
    """Loads the pre-trained face detection model."""
    prototxt_path = "./protocol/deploy.prototxt.txt"
    model_path = "./model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    return cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Global variable to store the model (avoids reloading it multiple times)
face_net = load_face_detection_model()

#save video function
def save_video(video, output_path):

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    res = (frame_width, frame_height)

    # Define the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
    out = cv2.VideoWriter(output_path, fourcc, fps, res)
    return  out

def blur_faces(image, confidence_threshold=0.5, blur_strength=61):
    """
    Detects and blurs faces in an image.

    Parameters:
        image (numpy.ndarray): Input image.
        confidence_threshold (float): Minimum confidence for face detection.
        blur_strength (int): Kernel size for Gaussian blur (must be odd).
    
    Returns:
        numpy.ndarray: Image with blurred faces.
    """
    (h, w) = image.shape[:2]

    # Prepare the image for the deep learning model
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 
        1.0, 
        (300, 300),
        (104.0, 177.0, 123.0)
    )
    
    # Perform detection
    face_net.setInput(blob)
    detections = face_net.forward()

    # Process detections
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
    
    return image


def blur_faces_images(image_path):
    """
    Load an image, blurs detected faces in each frame, and saves the output.

    Parameters:
        image_path (str): Path to the input image.
    """
    
    # Load and process the image
    image = cv2.imread(image_path)
    blurred_image = blur_faces(image) 
    
    # Create output folder
    name = os.path.basename(image_path)
    output_folder = "./output_images/"
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the processed image in the right folder
    output_path = os.path.join(output_folder, name)
    cv2.imwrite(output_path, blurred_image) 

def blur_faces_videos(video_path):
    """
    Processes a video, blurs detected faces in each frame, and saves the output.

    Parameters:
        video_path (str): Path to the input video.
    """
    
    name = os.path.basename(video_path)
    output_folder = "./output_videos/"
    os.makedirs(output_folder, exist_ok=True)

    # Ensure the output file has a valid extension
    output_path = os.path.join(output_folder, os.path.splitext(name)[0] + "_blurred.mp4")
    
    video, output_path, out= save_video(video_path)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        blurred_frame = blur_faces(frame)  # Apply face blurring
        cv2.imshow('Blurred Video', blurred_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

        out.write(blurred_frame)  # Save the processed frame

    # Release resources
    out.release()
    video.release()
    cv2.destroyAllWindows()
    print(f"Video saved at: {output_path}")


def blur_face_webcam():
    """
    Captures video from the webcam, applies face blurring in real-time, 
    and allows stopping the recording by pressing 'q'.
    """
    
    video = cv2.VideoCapture(0)  # Open webcam
    output_folder = "./output_videos/"
    os.makedirs(output_folder, exist_ok=True)

    # Ensure the output file has a valid extension
    output_path = os.path.join(output_folder, ("webcam_blurred.mp4"))
    
    out= save_video(video, output_path)
    while True:
        ret, frame = video.read()
        if not ret:
            break

        blurred_frame = blur_faces(frame)
        cv2.imshow('Blurred Webcam Feed', blurred_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        out.write(blurred_frame)  # Save the processed frame

    # Release resources
    out.release()
    video.release()
    cv2.destroyAllWindows()
    print(f"Video saved at: {output_path}")
    