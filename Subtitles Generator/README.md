# Subtitle Generator
----------


This script automatically generates subtitles (.srt files) from audio or video files using OpenAI's Whisper model. For video files, it can also create a new video file with soft subtitles embedded.

The tool supports specifying the language for transcription, improving accuracy for non-English content.

## How it works

1- For video files, it first extracts the audio track

2- Uses Whisper AI to transcribe the audio with timestamps

3- Generates a standard .srt subtitle file

4- Optionally creates a new video file with embedded subtitles


## Configuration

You can configure the behavior by modifying these parameters in main.py:

```
input_path (path to your audio/video file)

subtitle_path (output subtitle path)

model (Whisper model size medium or large)

mux (Boolean to specify whether or not to create the subtitled video)
```


## How to run 

### 1- Install dependencies
Before running the script, run the following command:
```
pip install -r requirements.txt
```

### 2- Install FFmpeg

- On windowns:
    - Download FFmpeg from https://ffmpeg.org/download.html#build-windows 
    - Add FFmpeg to your system path

- On linux:
    ```
    sudo apt update && sudo apt install ffmpeg
    ```
Verify installation with
```
ffmpeg -version
```

### 3- Run the script
Modify parameters and run
```
python main.py
```
The script will generate:
- A .srt subtitle file
- (For videos) A new video file with soft subtitles 

## Supported formats
Input formats:
- Video: .mp4, .avi, .mov and .mkv
- Audio: .wav, .mp3 (any other supported by Whisper)

Output formats:
- Subtitles: .srt
- Video: .mkv or .mp4

## Benefits
* Accurate transcription: Uses state-of-the-art Whisper AI for high-quality results
* Language support: Works with multiple languages (specify in transcribe() method)
Preserves quality: Original video quality es maintained when muxing