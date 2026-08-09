"""
pomodoro_timer.py

Author: Sal Balsamo
Date: 8/5/2026
Purpose: Create PomodoroTimer class for the Pomodoro functionality of TomoToro
"""

import time

class PomodoroTimer:
    def __init__(self, work_min=25, break_min=5, long_break_min=15, cycles_before_long_break=4):
        self.work_min = work_min
        self.break_min = break_min
        self.long_break_min = long_break_min
        self.cycles_to_long_break = cycles_before_long_break
        self.cycle_count = 0
        self.state = "work" # work, break, or long_break

    def next_state(self):
        if self.state == "work":
            self.cycle_count += 1
            if self.cycle_count % self.cycles_to_long_break == 0:
                self.state = "long_break"
            else:
                self.state = "break"
        else:
            self.state = "work"
        return self.state

    def to_dict(self):
        return {}