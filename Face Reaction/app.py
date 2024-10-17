import cv2
import numpy as np
from fer import FER
import os
import json

# Load custom emojis from a config file (custom_emojis.json)
def load_custom_emojis(config_file='custom_emojis.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    return {}

# Save the emotion detection history
def save_emotion_history(history, filename='emotion_history.txt'):
    with open(filename, 'a') as file:
        for emotion in history:
            file.write(f"{emotion}\n")

# Initialize the webcam
scr = cv2.VideoCapture(0)  # 30fps
scr.set(3, 640)
scr.set(4, 480)

# Initialize FER (Facial Expression Recognition)
detector = FER(mtcnn=True)

# Load custom emojis
custom_emojis = load_custom_emojis()

# Initialize emotion detection history
emotion_history = []

while True:
    ret, frame = scr.read()

    # Return emotion name and % of true detection
    emotion, score = detector.top_emotion(frame)

    # Append detected emotion to the history
    emotion_history.append(emotion)
    # Optionally save the history to a file (uncomment to enable)
    # save_emotion_history(emotion_history)

    print(emotion, score)

    # Use custom emoji if available, otherwise fall back to default
    if emotion in custom_emojis:
        emoj = cv2.imread(custom_emojis[emotion])
    else:
        # Default emojis if no custom emojis are set
        if emotion == 'angry':
            emoj = cv2.imread('https://i.ibb.co/QN0gqNH/angry.png')
        elif emotion == 'disgust':
            emoj = cv2.imread('https://i.ibb.co/tJDxrhD/disgust.png')
        elif emotion == 'fear':
            emoj = cv2.imread('https://i.ibb.co/yBczSFB/fear.png')
        elif emotion == 'happy':
            emoj = cv2.imread('https://i.ibb.co/g6DW0Cf/happy.png')
        elif emotion == 'sad':
            emoj = cv2.imread('https://i.ibb.co/NyF0sDq/sad.png')
        elif emotion == 'surprise':
            emoj = cv2.imread('https://i.ibb.co/D4rDyfM/surprise.png')
        elif emotion == 'neutral':
            emoj = cv2.imread('https://i.ibb.co/KX7VSjh/neutral.png')
        else:
            emoj = cv2.imread('https://i.ibb.co/LdnS9nL/none.png')

    # Adding Image on Screen
    # Read emoj and resize
    size = 150
    emoj = cv2.resize(emoj, (size, size))

    # Create a mask of emoj
    img2gray = cv2.cvtColor(emoj, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

    roi = frame[-size-20:-20, -size-20:-20]
    # Set an index of where the mask is
    roi[np.where(mask)] = 0
    roi += emoj

    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (40, 210)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    cv2.putText(frame, emotion, org, font, fontScale, color, thickness, cv2.LINE_AA)

    # Show screen
    cv2.imshow('frame', frame)

    # Stop
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release resources
scr.release()
cv2.destroyAllWindows()
