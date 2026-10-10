import yt_dlp  # pip install yt-dlp


def my_hook(d):
    if d['status'] == 'finished':
        print(f"Downloaded: {d['filename']}")


ydl_opts = {
    'ffmpeg_location': r'Youtube Downloader\bin',
    'progress_hooks': [my_hook],
    'outtmpl': '%(playlist_title)s/%(title)s.%(ext)s',
    'restrictfilenames': True,
}


def downloader():
    URLS = []

    question = input(
        "Do you want to download a playlist? (Y/n): "
    ).lower()

    if question == 'y':
        URLS.append(input("Enter Playlist URL: "))
        ydl_opts['noplaylist'] = False

    else:
        question = input(
            "Do you have more than one video to download? (Y/n): "
        ).lower()

        if question == 'y':
            while True:
                line = input(
                    "Enter Video URL or type (q) to start downloading: "
                )

                if line.lower() == 'q':
                    break

                if line:
                    URLS.append(line)

        else:
            URLS.append(input("Enter Video URL: "))

        ydl_opts['noplaylist'] = True

    if not URLS:
        print("No URLs provided.")
        return

    question = input(
        "Do you want audio output only? (Y/n): "
    ).lower()

    if question == 'y':
        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
    else:
        ydl_opts['format'] = (
            'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)


if __name__ == "__main__":
    downloader()
