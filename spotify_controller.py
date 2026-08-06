"""
spotify_controller.py

Author: Sal Balsamo
Date: 8/5/2026
Purpose: Link user's Spotify account to the program using Spotipy
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = "9dbe36fad08e44f5a49e70a03b12eb19"
    client_secret = "f979f6585a1b43de9903382071afa4ca"
    redirect_uri = "http://[::1]:8888/callback"
    scope = "user-modify-playback-state user-read-playback-state playlist-read-private"
    ))

playlists = sp.current_user_playlists()