import sys
import spotipy
import json
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

USERNAME = os.getenv('USERNAME')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

scope = """ user-modify-playback-state, 
            user-library-read, 
            user-read-playback-state,
            playlist-read-private, 
            playlist-modify-public, 
            playlist-modify-private """

token = SpotifyOAuth(scope = scope, client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI)
spotify = spotipy.Spotify(auth_manager = token)

def parser():
    raw_input = input("Enter command: ")
    raw_input = raw_input.lower()

    match raw_input:
        case "pause" | "stop":
            stop_playback()
        case "play" | "start":
            start_playback()
        case "current" | "c":
            get_current_track_info()
        case "skip" | "next" | "n":
            skip_track()
        case "back" | "previous":
            previous_track()
        case "quit" | "q" | "terminate":
            sys.exit()
        case "new_playlist" | "create_playlist":
            create_new_playlist()
        case "delete_playlist" | "remove_playlist":
            delete_playlist()
        case "playlists":
            show_playlists()
        case "t" | "Test":
            print("Test case.")
            test()
        case "connect":
            # Is it possible to make a connection? every the device goes to sleep it can not connect.
            return ""
        case _:
            print(f"Command not exepted: {raw_input}")

def start_playback():
    try:
        spotify.start_playback()
    except:
        print("Illegal command play, already playing, else check connection.")

def stop_playback():
    try:
        spotify.pause_playback()
    except:
        print("Illegal command, already paused, else check connection ")

def skip_track():
    try:
        spotify.next_track()
    except:
        print("", end="")

def previous_track():
    try:
        spotify.previous_track()
    except:
        print("", end="")

def get_current_track_info():
    try:
        result = spotify.current_playback() # Needed to keep for progress.
        print(f"{convert_ms_to_time(result['progress_ms'])} - {convert_ms_to_time(result['item']['duration_ms'])}")
        track = spotify.track(result['item']['id'])
        print("\nTrack Information: \n")
        print(track['name'])
        print(track['album']['name'])
        print(string_with_more_than_one_artist(track))
        print(f"{convert_ms_to_time(result['progress_ms'])} - {convert_ms_to_time(track['duration_ms'])}")
        print(f"Playing: {result['is_playing']}")
        print(f"Shuffle: {result['shuffle_state']}")
        #print(f"playlist: {result['context']}") # Contains information about playlist URi, URL..
        print("\n")
    except:
        print("", end="")

def convert_ms_to_time(current_time_ms):
    time = timedelta(milliseconds = current_time_ms) # Contains seconds, hours and days.

    if(time.seconds >= 60 * 60): # Minutes and seconds.
        hours = int(time.seconds / 60 / 60)
        minutes = (time.seconds - hours * 60 * 60) / 60
        return f"{hours}:{minutes}:{seconds}" # No 0 formatting for time with hours.

    minutes = int(time.seconds / 60)
    seconds = time.seconds - minutes * 60
    return f"{minutes}:{seconds}" if seconds > 10 else f"{minutes}:0{seconds}"

def string_with_more_than_one_artist(track):
    artists = track['artists']
    artists_string = ""
    for artist in artists:
        if artists_string != "":
            artists_string += ", "
        artists_string += artist['name']

    return artists_string

def get_track_with_spotify_id(spotify_id):
    return spotify.track(spotify_id)

def show_playlists():
    try:
        playlists = spotify.current_user_playlists()
        for playlist in playlists['items']:
            print(f"{playlist['name']} - Spotify id: {playlist['id']}")
    except:
        print("", end="")

# TODO: check if the playlist name is taken in the users saved playlists.
def create_new_playlist():
    try:
        playlist_name = input("Playlist name: ")
        playlist_name.strip()
        public = yes_or_no_input_to_bool() # Apparently my loocal Spotify states that it is public no matter the input...
        description = input("description: ")
        spotify.user_playlist_create(user = USERNAME, name = playlist_name, public = public, description = description)
    except:
        print("Illegal arguments.")

def delete_playlist():
    spotify.current_user_unfollow_playlist("7oUtJpCMDIi7fJ2iOjdfOy")

def yes_or_no_input_to_bool():
    public = ''
    while len(public) != 1:
        public = input("Publiv y/n: ")
        public = public.lower()
        if public != 'y' and public != 'n':
            public = ""
            print("Illegal argument, needs to be y or n.")

    return True if public == 'y' else False

def test():
    return ""

while(True):
    parser()
