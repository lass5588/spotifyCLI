import sys
import spotipy
import json
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "user-modify-playback-state, user-library-read, user-read-playback-state"

token = SpotifyOAuth(scope = scope, client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI)
spotify = spotipy.Spotify(auth_manager = token)

def parser():
    print("enter command: ", end="")
    raw_input = input()

    match raw_input:
        case "pause" | "Pause" | "PAUSE" | "start" | "Start" | "START":
            stop_playback()
        case "play" | "Play" | "PLAY" | "stop" | "Stop" | "STOP":
            start_playback()
        case "current" | "Current" | "CURRENT" | "c" | "C":
            get_current_track_info()
        case "skip" | "Skip" | "SKIP" | "next" | "Next" | "NEXT" | "n" | "N":
            skip_track()
        case "back" | "Back" | "BACK" | "previous" | "Previous" | "PREVIOUS":
            previous_track()
        case "quit" | "Quit" | "QUIT" | "Q" | "q" | "terminate":
            sys.exit()
        case "t":
            print("Test case.")
            test()
        case "Connect":
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
    
def test():
    return ""

while(True):
    parser()
