"""
Author: https://github.com/AcidOP
"""

import os
import pafy # pip install pafy
from httpx import main # pip install httpx
from youtubesearchpython import VideosSearch # pip install youtube-search-python


def fetchVideoId():
    song = input('[#] Name of the video > ')

    video_obj = VideosSearch(song, limit=1)
    # Video id of the song
    id = video_obj.result()['result'][0]['id']

    return id


def download():
    id = fetchVideoId()

    video = pafy.new(id)

    isVideo = input("Is it to be sasved as Video? (Y/N): ")

    if isVideo.lower() == "y":
        best = video.getbest()
    else:
        best = video.getbestaudio()

    video_name = f"{best.title}.{best.extension}"
    current_dir = os.getcwd()
    # Create a folder to save the video
    if not os.path.exists(f"{current_dir}/videos"):
        os.mkdir(f"{current_dir}/videos")
    # Save the video
    print(f"[#] Downloading {video_name}...")
    best.download(filepath=f"{current_dir}/videos/{video_name}")
    print(f"[#] Downloaded {video_name}!")


if __name__ == "__main__":
    download()
