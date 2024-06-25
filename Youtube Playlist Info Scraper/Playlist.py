"""
This module provides functionalities for YouTube Playlist.
"""

import requests
from bs4 import BeautifulSoup
import json

class Playlist:

    """
    This class provides methods to perform operatoins for given YouTube Playlist.
    """

    def __init__(self, playlist_link):
        
        """
        Initializes the playlist with a playlist link.

        Parameters:
            playlist_link (str): Url of YouTube Playlist
        """

        self.playlist_link = playlist_link

    def info(self):

        """
        Returns:
            dict: Information about given Playlist.
        """

        info = {}

        try:

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36"}

            response = requests.get(url=self.playlist_link, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')

            script_elements = soup.find_all('script')

            for e in script_elements:

                if e.text.startswith("var ytInitialData"):
                   
                    data_dict = json.loads(e.text[20:-1])

                    playlist = data_dict["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]
                    
                    if "title" in playlist:
                        info["title"] = playlist["title"]
                    else:
                        info["title"] = ""

                    if "totalVideos" in playlist:
                        info["totalVideos"] = playlist["totalVideos"]
                    else:
                        info["totalVideos"] = ""

                    if "ownerName" in playlist:
                        info["channelName"] = playlist["ownerName"]["simpleText"]
                    else:
                        info["channelName"] = ""

                    if "playlistShareUrl" in playlist:
                        info["playlistUrl"] = playlist["playlistShareUrl"]
                    else:
                        info["playlistUrl"] = ""

                    if "contents" in playlist:

                        playlist_videos = playlist["contents"]

                        info["videos"] = []

                        for video in playlist_videos:

                            video_data = {}

                            video = video["playlistPanelVideoRenderer"]

                            if "title" in video:
                                video_data["title"] = video["title"]["simpleText"]
                            else:
                                video_data["title"] = ""

                            if "lengthText" in video:
                                video_data["duration"] = video["lengthText"]["simpleText"]
                            else:
                                video_data["duration"] = ""

                            if "videoId" in video:
                                video_data["id"] = video["videoId"]
                            else:
                                video_data["id"] = ""

                            info["videos"].append(video_data) # Update info with video

                    info["duration"] = self.__calculatePlaylistDuration(info["videos"])

                    break # Target Element Found; Break loop

        except Exception as e:
            print("Error in info():", e)

        return info
    
    def __calculatePlaylistDuration(self, videos_data):
        
        """
        Calculate total playlist duration by aggregating the duration of all videos present in playlist.

        Parameters:
            list: List of videos' data
        
        Returns:
            str: Total duration of Playlist Videos in format -> HH:MM:SS
        """

        total_duration = "00:00:00"

        try:

            hours, minutes, seconds = 0,0,0

            for video in videos_data:

                video_duration = video["duration"]

                video_duration_parts = video_duration.split(":")
                
                if len(video_duration_parts) == 3:
                    hours += int(video_duration_parts[0])
                    minutes += int(video_duration_parts[1])
                    seconds += int(video_duration_parts[2])
                
                if len(video_duration_parts) == 2:
                    minutes += int(video_duration_parts[0])
                    seconds += int(video_duration_parts[1])
                
                if len(video_duration_parts) == 1:
                    seconds += int(video_duration_parts[0])

            hours += minutes // 60

            minutes = minutes % 60

            minutes += seconds // 60

            seconds = seconds % 60

            total_duration = f"{hours}:{minutes}:{seconds}"

        except Exception as e:
            print("Error in __calculatePlaylistDuration():", e)

        return total_duration