import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = 'playlist-modify-public'

token = SpotifyOAuth(scope=scope)
spotifyObject = spotipy.Spotify(auth_manager = token)

spotifyObject.user_playlist_create(name="randomTest",public=True,description="just something")