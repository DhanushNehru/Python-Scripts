# Mood Based Youtube Song Generator
This Python script fetches a random song from YouTube based on your mood input and opens it in your default web browser.

## Features
Accepts mood input (e.g., happy, sad, energetic) and finds related songs on YouTube.
Opens the YouTube song URL in your browser.

## Setup

### 1. Install dependencies:
```shell
pip install -r requirements.txt
```

### 2. Get your YouTube API key:
- Follow the instructions to get your YouTube Data API key.

### 3. Set your API key:
Replace the api_key variable in the script with your own [YouTube Data API key](https://developers.google.com/youtube/v3/getting-started)
```python
api_key = "YOUR_YOUTUBE_API_KEY"
```

### 4. Run the script:
```shell
python random_song_generator.py
```

## Example
Input:
```bash
Enter your mood (e.g., happy, sad, energetic): happy
```
The script will fetch a song and open it in your browser.

