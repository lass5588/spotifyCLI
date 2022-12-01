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
        case "p":
            play_or_pause()
        case "repeat":
            toggle_repeat_mode()
        case "repeat track":
            toggle_repeat_single_track()
        case "shuffle":
            toggle_shuffle_mode()
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
        case "tracks":
            show_tracks_in_playlist("564dMLmDhjO0jssao6w9mK")
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

def play_or_pause():
    try:
        playback_state = get_current_playback()
        stop_playback() if playback_state["is_playing"] else start_playback()
    except:
       print("Current playback can not be accessed, check connection. ", end="")

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

# The third option "track" (repeating same track) can not be set, but if it is set it will be toggled off.
def toggle_repeat_single_track():
    try:
        playback = get_current_playback()
        spotify.repeat("track") if playback["repeat_state"] != "track" else spotify.repeat("off")
    except:
        print("Repeat mode can not be toggled, check connection. ")

def toggle_repeat_mode():
    try:
        playback = get_current_playback()
        
        if playback["repeat_state"] == "off" or playback["repeat_state"] == "track":
            spotify.repeat("context")
        if playback["repeat_state"] == "context":
            spotify.repeat("off")
    except:
        print("Repeat mode can not be toggled, check connection. ")

def toggle_shuffle_mode():
    try:
        playback = get_current_playback()
        spotify.shuffle(False) if playback["shuffle_state"] == True else spotify.shuffle(True)
    except:
        print("Shuffle mode can not be toggled, check connection. ")

def get_current_track_info():
    try:
        current_playback = get_current_playback() # Needed to keep for progress.
        track = get_track_with_spotify_id(current_playback['item']['id'])
    except:
        print("Current playback can not be accessed, check connection. ", end="")
    
    print("\nTrack Information: \n")
    print(track['name'])
    print(track['album']['name'])
    print(string_with_more_than_one_artist(track))
    print(f"{convert_ms_to_time(current_playback['progress_ms'])} - {convert_ms_to_time(track['duration_ms'])}")
    print(f"Playing: {current_playback['is_playing']}")
    print(f"Shuffle: {current_playback['shuffle_state']}")
    #print(f"playlist: {current_playback['context']}") # Contains information about playlist URi, URL..
    print("\n")

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

def get_current_playback():
    try:
        return spotify.current_playback()
    except:
        print("Current playback can not be accessed, check connection. ", end="")

def get_track_with_spotify_id(spotify_id):
    try:
        return spotify.track(spotify_id)
    except:
        print("Track id can not be found. ", end="")

def get_playlist_with_spotify_id(spotify_id):
    try:
        return spotify.playlist(spotify_id)
    except:
        print("Playlist id can not be found. ", end="")

def show_playlists():
    try:
        playlists = spotify.current_user_playlists()
        for playlist in playlists['items']:
            print(f"{playlist['name']} - Spotify id: {playlist['id']}")
    except:
        print("", end="")

def show_tracks_in_playlist(playlist_id):
    playlist = get_playlist_with_spotify_id(playlist_id) # print(playlist['tracks']['items'][0]['track']['name']) The complete path.
    tracksObject = playlist['tracks']
    tracks = tracksObject['items']

    try:
        while tracksObject['next']:
            tracksObject = spotify.next(tracksObject)
            tracks.extend(tracksObject['items'])
    except:
        print("illegal next id. ", end="")

    for i, item in enumerate(tracks):
        track = item['track'] # can not be specied in the enumerate
        print(f"{i}: {track['name']}")

# TODO check if the playlist name is taken in the users saved playlists.
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
        public = input("Public y/n: ")
        public = public.lower()
        if public != 'y' and public != 'n':
            public = ""
            print("Illegal argument, needs to be y or n.")

    return True if public == 'y' else False

def test():
    return ""

while(True):
    parser()
