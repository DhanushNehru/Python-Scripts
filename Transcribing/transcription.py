import sys
import subprocess
import shutil

#functions to isntall python packages
def installPackage(pkgName):
    print(f"[INFO] {pkgName} not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkgName])
    print(f"[INFO] {pkgName} installed successfully!")

try:
    from faster_whisper import WhisperModel
except ImportError:
    installPackage("faster_whisper")
    from faster_whisper import WhisperModel

# Check for ffmpeg
if shutil.which("ffmpeg") is None:
    print(
        "[ERROR] ffmpeg not found on your system.\n"
        "Please install ffmpeg to use this script:\n"
        "- Windows: https://ffmpeg.org/download.html\n"
        "- Linux: sudo apt install ffmpeg\n"
        "- Mac: brew install ffmpeg"
    )
    sys.exit(1)

print("[INFO] All dependencies are ready!")

audio_file = input("Enter the path to your audio file (MP3, WAV, MP4 etc.): ").strip()
valid_models = ["tiny", "small", "base", "medium", "large"]
print("Models (Sorted from Fastest-Smallest-Least Accurate To Slowest-Largest-Most Accurate):-\n")
print("Make Sure to write .en after writing model name if you only want english transcription (Less work for model)\n")
print(valid_models)
model_size = input("\nEnter the model size: ").strip().lower()

if model_size not in valid_models:
    print(f"[ERROR] Invalid model size '{model_size}'. Please choose from {valid_models}.")
    sys.exit(1)

model = WhisperModel(model_size)

import os
if not os.path.isfile(audio_file):
    print(f"[ERROR] File '{audio_file}' does not exist. Please check the path and try again.")
    sys.exit(1)

output_file = audio_file.rsplit(".", 1)[0] + "_transcript.txt"
segments, info = model.transcribe(audio_file)

with open(output_file, "w", encoding="utf-8") as f:
    for segment in segments:
        f.write(segment.text + "\n")
print(f"[INFO] Transcription saved to {output_file}")
print("\n -- Scripted by Syed Sultan (github = Syed-56)")