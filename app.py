"""
app.py

Author: Sal Balsamo
Date: 8/8/2026
Purpose: Main entry point for the TomoToro application, sets up Flask server and routes
"""

from flask import Flask, render_template
from pomodoro_timer import PomodoroTimer
app = Flask(__name__)

timer = PomodoroTimer()

@app.route("/")
def index():
    return render_template("index.html",timer_state=timer.state)

# @app.route("/api/")

@app.route("/api/next_state")
def api_next_state():
    return timer.next_state()

if __name__ == "__main__":
    app.run(debug=True)