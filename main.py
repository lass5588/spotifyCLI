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
        case "pause" | "Pause" | "PAUSE":
            stop_playback()
        case "play" | "Play" | "PLAY":
            start_playback()
        case "current" | "Current" | "CURRENT":
            get_current_track()
        case "skip" | "Skip" | "SKIP" | "next" | "Next" | "NEXT":
            skip_track()
        case "back" | "Back" | "BACK" | "previous" | "Previous" | "PREVIOUS":
            previous_track()
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

def get_current_track():
    try:
        result = spotify.current_playback()
        print(result['device']['is_active'], " – ", result['progress_ms']/1000,)
    except:
        print("", end="")

while(True):
    parser()
