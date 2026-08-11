"""
spotify_controller.py

Author: Sal Balsamo
Date: 8/5/2026
Purpose: Link user's Spotify account to the program using Spotipy
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from flask import request

load_dotenv()

env_client_id = os.getenv("SPOTIFY_CLIENT_ID")
env_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp_oauth = SpotifyOAuth(
    client_id = env_client_id,
    client_secret = env_client_secret,
    redirect_uri = "http://127.0.0.1:5000/callback",
    scope = "user-modify-playback-state user-read-playback-state playlist-read-private"
    )

sp = spotipy.Spotify(auth_manager=sp_oauth)

def get_login_url():
    return sp_oauth.get_authorize_url()

def code_for_token(code):
    return sp_oauth.get_access_token(code)

def get_playlists_sp():
    playlists_data = sp.current_user_playlists()

    global playlist_dict
    playlist_dict = {}
    for playlist in playlists_data["items"]:
        name = playlist["name"]
        uri = playlist["uri"]
        playlist_dict[name] = uri
    return playlist_dict

def play_playlist(uri):
    sp.start_playback(context_uri=uri)

def pause_playback():
    if sp.current_playback().get("is_playing"):
        sp.pause_playback()

def resume_playback():
    if not sp.current_playback().get("is_playing"):
        sp.start_playback()

def stop_playback():
    sp.pause_playback()