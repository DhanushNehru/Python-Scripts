import yt_dlp # pip install yt-dlp

def my_hook(d):
    if d['status'] == 'finished':
        print(f"Done downloading, now post-processing ... File saved as: {d['filename']}")

ydl_opts = {
    'ffmpeg_location': r'Youtube Downloader\bin',
    'progress_hooks': [my_hook],
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': 'True',
}


def downloader():
    URLS = []
    question = input("Do you have more than one video you'd like to download? (Y/n): ").lower()
    if question == 'y':
        while True:
            line = input("Enter Video URL or type (q) to start downloading: ")
            if line.lower() == 'q':
                break
            else:
                URLS.append(line)
    else:
        URLS.append(input('Enter Video URL: '))

    question = input("Do you want audio output only (Y/n): ").lower()
    if question == 'y':
        ydl_opts['format'] = 'bestaudio[ext=m4a]/best,'
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best,'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)
    
if __name__ == "__main__":
    downloader()