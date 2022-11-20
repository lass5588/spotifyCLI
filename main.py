import sys
import spotipy
import json
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

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
        case "current" | "Current" | "CURRENT":
            get_current_track_info()
        case "skip" | "Skip" | "SKIP" | "next" | "Next" | "NEXT":
            skip_track()
        case "back" | "Back" | "BACK" | "previous" | "Previous" | "PREVIOUS":
            previous_track()
        case "quit" | "Quit" | "QUIT" | "Q" | "q" | "terminate":
            sys.exit()
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
        result = spotify.current_playback()
        print(f"Track: {result['item']['name']}")
        print(f"Album: {result['item']['album']['name']}")
        print(f"Artist: {result['item']['artists'][0]['name']}") # prints only the first currently [0], will fail if more is selected without having one.
        print(f"Playing: {result['is_playing']}")
        print(result['device']['is_active'], " – ", result['progress_ms']/1000,)
        # Present time => 2:35 of 3:45
    except:
        print("", end="")

while(True):
    parser()
