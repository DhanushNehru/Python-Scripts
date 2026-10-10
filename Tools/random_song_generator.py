import random
import webbrowser
from googleapiclient.discovery import build


def fetch_youtube_songs(mood):
    api_key = "your_youtube_api_key"
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        q=f"{mood} song", part="snippet", type="video", maxResults=10
    )
    response = request.execute()
    songs = [
        f"{item['snippet']['title']} - https://www.youtube.com/watch?v={item['id']['videoId']}"
        for item in response['items']
    ]
    return songs


def random_song_generator():
    mood = input("Enter your mood (e.g., happy, sad, energetic): ").lower()
    try:
        songs = fetch_youtube_songs(mood)
        random_song = random.choice(songs)
        song_title, song_url = random_song.split(" - ")
        webbrowser.open(song_url)
        print(f"Here's a song for your mood ({mood}):\n{random_song}")
    except Exception as e:
        print("Error fetching songs. Please check your API key and mood.")


if __name__ == "__main__":
    random_song_generator()
