# MUST READ BEFORE EXECUTION (ONE TIME ONLY)

This script allows you to **transcribe audio files (MP3, WAV, etc.) to text** using the **Faster Whisper** Python library. Please read these instructions carefully before running the script.  

---

## 1️⃣ Prerequisites

1. **Install Python (3.8 or higher)**  
   Download and install from [https://www.python.org/downloads/](https://www.python.org/downloads/).  
   Make sure to **add Python to your system PATH** during installation.
   OR you can simply run this command in terminal to install python: "winget install Python.Python.3"
   for MAC: brew install python

2. **Install ffmpeg** (required for audio decoding)  
   - **Windows:** [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
   - **Linux:** `sudo apt install ffmpeg`  
   - **Mac:** `brew install ffmpeg`  
   Make sure ffmpeg is **added to your system PATH** so the script can find it. (Explanation in End on how to do this)
    Now you can verify if both are installed by writing "python --version" or "py --version" and "ffmpeg -version"
---

## 2️⃣ Audio File Requirements

- Place the audio file you want to transcribe **in the same folder** as the script.  
- Make sure to use the **correct file extension** (e.g., `.mp3`, `.wav`). 
- Also works for videos (.mp4)
- The output transcription will also be saved in the same folder with the filename:  


---

## 3️⃣ Choosing the Model

The script supports the following **Faster Whisper models**. Please choose the one that fits your needs:

| Model   | Speed & Size                 | Accuracy                     |
|---------|------------------------------|-------------------------------|
| tiny    | Fastest, smallest            | Least accurate               |
| small   | Fast, small                  | Slightly more accurate       |
| base    | Moderate speed & size        | Good accuracy                |
| medium  | Slower, larger               | More accurate                |
| large   | Slowest, largest             | Most accurate                |

**Tip:** Use `base` for a good balance between speed and accuracy. Model names are **case-insensitive**.

---

## 4️⃣ Running the Script

1. Open a terminal or command prompt in the folder containing the script.  
2. Run the script: type "python transcription.py"
3. Follow Along the input instructions prompted on screen

## 5 Setting ffmpeg in Your System PATH

To make ffmpeg accessible to the script:

**Windows:**  
1. Download and unzip ffmpeg.  
2. Copy the path to the `bin` folder (e.g., `C:\ffmpeg\bin`).  
3. Open **Environment Variables → Path → Edit → New**, paste the path, and click **OK**.  
4. Restart the terminal or command prompt.

**Linux / Mac:**  
write export PATH=$PATH:/path/to/ffmpeg/bin

## Developer
- GitHub: https://github.com/Syed-56
- LinkedIn: https://www.linkedin.com/in/syedsultan10

## Dependencies & Licenses
- Faster Whisper: MIT License (https://github.com/guillaumekln/faster-whisper)
- ffmpeg: LGPL/GPL License (https://ffmpeg.org)