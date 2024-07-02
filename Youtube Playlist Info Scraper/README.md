## YouTube Playlist Info Scraper

This python module retrieve information about a YouTube playlist in json format using playlist link.

### Usage:

Install dependencies:

    pip install -r requirements.txt

Import module:

    from Playlist import Playlist

Create Object:

    playlist = Playlist("PLAYLIST_LINK_HERE") # Example: https://www.youtube.com/watch?v=_t2GVaQasRY&list=PLeo1K3hjS3uu_n_a__MI_KktGTLYopZ12

Retrieve Playlist Info:

    info = playlist.info()
    print(info)

### Output Format:

```
    {
        "title": ..., 
        "totalVideos": ..., 
        "channelName": ..., 
        "playlistUrl": ..., 
        "duration": ...,
        "videos": [
            {
                "title": ..., 
                "duration": ..., 
                "id": ...
            }
            , 
            .
            .
            .
            ], 
    }
```

<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->