"""
app.py

Author: Sal Balsamo
Date: 8/8/2026
Purpose: Main entry point for the TomoToro application, sets up Flask server and routes
"""

from flask import Flask, render_template, request, jsonify, redirect
from pomodoro_timer import PomodoroTimer
from spotify_controller import *

app = Flask(__name__)
timer = PomodoroTimer()

@app.route("/")
def index():
    return render_template("index.html",timer_state=timer.state)

@app.route("/api/next-state")
def api_next_state():
    timer.next_state()
    return jsonify(timer.to_dict())

@app.route("/api/get-settings")
def get_settings():
    return jsonify(timer.to_dict())

@app.route("/api/set-settings", methods=["POST"])
def set_settings():
    data = request.get_json()
    global timer
    timer = PomodoroTimer(
        work_min=int(data["work_min"]),
        break_min=int(data["break_min"]),
        long_break_min=int(data["long_break_min"]),
        cycles_before_long_break=int(data["cycles_before_long_break"])
    )
    global current_playlist_name
    current_playlist_name = data["playlist_name"]
    return jsonify(timer.to_dict())

@app.route("/api/play-music", methods=["POST"])
def play_music():
    play_playlist(current_playlist_name)
    return "Now playing:" + current_playlist_name

@app.route("/api/toggle-music", methods=["POST"])
def toggle_music():
    toggle_playback()
    return "Playback toggled"

@app.route("/api/stop-music", methods=["POST"])
def stop_music():
    stop_playback()
    return "Playback stopped"

@app.route("/login")
def login():
    return redirect(get_login_url())

@app.route("/callback")
def callback():
    code_for_token(request.args.get("code"))
    return redirect("/")

@app.route("/api/get-playlists")
def get_playlists():
    return jsonify(get_playlists_sp())

# @app.route("/api/set-playlist", methods=["POST"])
# def set_playlists():
#     return 

if __name__ == "__main__":
    app.run(debug=True)