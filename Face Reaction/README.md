
# Face Reaction with Custom Emojis and Emotion History

This project uses OpenCV and FER (Facial Expression Recognition) to capture live video from the webcam, detect facial expressions in real time, and display corresponding emoji images for each detected emotion. Additionally, this enhanced version features custom emoji support and emotion detection history tracking, which provides a list of recently detected emotions.




## Acknowledgements

 We would like to express our sincere gratitude to the following:

OpenCV for providing powerful tools for computer vision, enabling us to process real-time video feeds with ease.

FER (Facial Expression Recognition) for simplifying the process of emotion detection with advanced facial expression recognition algorithms.

The open-source community for providing constant support, knowledge, and resources that have helped improve and evolve this project.

Contributors to this repository for their efforts in enhancing the functionality and maintaining the quality of the code.

Special thanks to all the libraries, frameworks, and developers whose work has made this project possible!


## Features Added to Project 

Real-Time Emotion Detection:

The system detects emotions such as angry, happy, sad, surprise, and more in real time using the FER library.
Custom Emojis:

Users can provide their own custom emoji images to represent emotions.
Emotion Detection History:

The program keeps track of the last 10 detected emotions and displays them on the screen, allowing users to see the emotion flow during the session.
Smooth Emoji Overlay:

The corresponding emoji for the detected emotion is displayed on the video feed in a designated corner of the screen.
## Prerequisites

Ensure that you have the following installed before running the script:

Python 3.x
OpenCV
Numpy
FER (Facial Expression Recognition)

You can install the required libraries by running:
pip install opencv-python numpy fer


## How to Run

Clone the Repository :

git clone https://github.com/your-repo/face-reaction.git

Run the Python script:

python face_reaction.py


## Custom Emoji Support

To add your custom emoji, replace the URLs or paths in the script with the path to your custom emoji image files. The supported emotions include angry, happy, sad, disgust, fear, surprise, and neutral.


## Code Explanation

Emotion Detection: The FER library is used to detect the dominant emotion in the video frame, with the highest probability score.

Custom Emoji Overlay: Based on the detected emotion, the corresponding emoji image is resized and overlaid on the video feed.

Emotion History: The recent emotions are displayed at the top-left corner of the video frame, showing the last 10 detected emotions during the session.


## Future Improvements 

Support for additional facial expressions.
Integration with cloud services for storing emotion history.