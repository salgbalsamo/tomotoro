"""
app.py

Author: Sal Balsamo
Date: 8/8/2026
Purpose: Main entry point for the TomoToro application, sets up Flask server and routes
"""

from flask import Flask, render_template, request, jsonify
from pomodoro_timer import PomodoroTimer
app = Flask(__name__)

timer = PomodoroTimer()

@app.route("/")
def index():
    return render_template("index.html",timer_state=timer.state)

@app.route("/api/next_state")
def api_next_state():
    timer.next_state()
    return jsonify(timer.to_dict())

@app.route("/api/get_settings")
def get_settings():
    return jsonify(timer.to_dict())

@app.route("/api/set_settings", methods=["POST"])
def set_settings():
    data = request.get_json()
    global timer
    timer = PomodoroTimer(
        work_min=int(data["work_min"]),
        break_min=int(data["break_min"]),
        long_break_min=int(data["long_break_min"]),
        cycles_before_long_break=int(data["cycles_before_long_break"])
    )
    return jsonify(timer.to_dict())

if __name__ == "__main__":
    app.run(debug=True)