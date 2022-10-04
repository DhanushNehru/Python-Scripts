from pytube import YouTube
import os

def get_song_list():
    music_data = []
    with open('./music-list.txt', 'r') as sl:
        music_list = sl.readlines()
        for _, music in enumerate(music_list): 
            music = music.replace('\n', '')
            music = music.split(' https:')
            music[1] = f'https:{music[1]}'
            music_data.append(music)
    return music_data


def run():
    music_data = get_song_list()

    for _, (title, url) in enumerate(music_data):
        # url input from user
        yt = YouTube(url)
        
        # extract only audio
        print(f"Extracting audio of: {title}")
        video = yt.streams.filter(only_audio=True).first()
        
        # check for destination to save file
        destination = "./music"
        
        # download the file
        print(f"Downloading: {title}")
        out_file = video.download(output_path=destination)
        
        # save the file
        new_filename = title + ".mp3"
        new_file = os.path.join(destination, new_filename)
        os.rename(out_file, new_file)
        
        # result of success
        print(yt.title + " has been successfully downloaded.")
        print('-' * 20)

    print("### All music files have been successfully downloaded! ###")

if __name__ == '__main__':
    run()
