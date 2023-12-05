from ytmusicapi import YTMusic as yt
import re
import pandas as pd
import requests as rq
import json
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import time
import spotipy.util as util
import fuzzywuzzy as fw
from fuzzywuzzy import fuzz


ytmusic = yt('headers_auth.json')

def yt_tracks(ytmusic,playlist_yt):
    list_yt_tracks = []
    playlist_yt_details = ytmusic.get_playlist(playlist_yt, limit = 1000)
    tracks_yt = playlist_yt_details['tracks']
    for tracks in tracks_yt:
        list_yt_tracks.append({'title':tracks['title'],'artist':tracks['artists'][0]['name'],'album':('None' if tracks['album'] is None else tracks['album']['name']),'duration':(tracks['duration'] if 'duration' in tracks else 'None')})
    df_yt_tracks = pd.DataFrame(list_yt_tracks)
    df_yt_tracks['title'] = df_yt_tracks['title'].apply(lambda x:(re.sub(r'\([^()]*\)','',x)).strip())
    return df_yt_tracks

def spotify_authorization(spotify_username,client_id,client_secret,scope):
    auth_mgr = util.prompt_for_user_token(spotify_username,scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost:8080') 
    sp = spotipy.Spotify(auth = auth_mgr)
    return sp

def new_playlist(spotify_username,sp,playlist_name,des):
    # playlist_name = 'Test Playlist'
    # des = "Testing Purpose"
    new_playlist_info = sp.user_playlist_create(spotify_username,playlist_name,description = des)
    print("Playlist Created")
    return new_playlist_info['id']

def get_spotify_song_list(df_yt_tracks):
    spotify_track_ids = []
    for track in df_yt_tracks.index:
        results = sp.search(q= '{} {}'.format(df_yt_tracks['title'].iloc[track], df_yt_tracks['artist'].iloc[track]) ,limit=5, type ='track')
        if results['tracks']['total']>0:
            for i in results['tracks']['items']:
                i['name'] = re.sub(r'\([^()]*\)','',i['name']).strip()
                if fuzz.partial_ratio(i['name'], df_yt_tracks['title'].iloc[track]) >90 and fuzz.partial_ratio(i['artists'][0]['name'],df_yt_tracks['artist'].iloc[track])>60:
                    spotify_track_ids.append(i['id'])
                    # track_names.append(df_yt_tracks['title'].iloc[track])
                    break
    print("Found suitable match of "+str(len(spotify_track_ids))+ " songs in Spotify Library!")
    return spotify_track_ids

def add_to_spotify(sp,newly_spotify_playlist_id, spotify_songs_list,spotify_username):
    while spotify_songs_list:
        sp.user_playlist_add_tracks(spotify_username, newly_spotify_playlist_id, spotify_songs_list[:90])
        spotify_songs_list = spotify_songs_list[99:]
    print("Songs added sucessfully! :)")

user_profile = input("Enter the Library link of your profile: \n")
user_yt = user_profile.split('/')[-1]

playlist_link = input("Enter the Playlist link of your profile: \n")
playlist_yt = playlist_link.split("=")[-1]

df_yt_tracks = yt_tracks(ytmusic,playlist_yt)

# https://open.spotify.com/user/v52avba3w6pkkxosgeglngh2c
spotify_username = input("Please enter your spotify username url/uri/shareable link:\n")
spotify_username = spotify_username.split('/')[-1]

client_id = "f23579cc015b4e518158755fd63d46fc"
client_secret = "9dd9fb72962e4c3f9d42474c0142313a"
scope = 'playlist-modify-public'

sp = spotify_authorization(spotify_username,client_id,client_secret,scope)

playlist_name = input("Give a name to your newly created playlist:\n")
des = input("Please Provide the description if any:\n")

newly_spotify_playlist_id = new_playlist(spotify_username,sp,playlist_name,des)

print("Finding the most accurate songs in Spotify Library\n It might take few minutes...Please Wait :)")
spotify_songs_list = get_spotify_song_list(df_yt_tracks)

add_to_spotify(sp,newly_spotify_playlist_id, spotify_songs_list,spotify_username)

# https://music.youtube.com/channel/UCLcvWDLANmp4g4dWOdMCoVg
# https://music.youtube.com/playlist?list=PLLT7phSFVy-lfNrRTXR_A_HiIpjL5IAEz
