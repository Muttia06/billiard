# cue.py
"""
Keterangan singkat: Modul cue.py mengurus mekanik stick/cue, aiming dan power. UI (drag) akan
menggunakan state dari Cue untuk menghitung impulse ke bola putih.
"""
from math import atan2, cos, sin
from ball import Vec2

class Cue:
    def __init__(self):
        self.aim_angle = 0.0
        self.power = 0.0
        self.max_power = 1000.0  # tunable
        self.charging = False

    def start_aim(self, from_pos, to_pos):
        dx = from_pos.x - to_pos.x
        dy = from_pos.y - to_pos.y
        self.aim_angle = atan2(dy, dx)

    def set_power_by_drag(self, drag_len):
        # drag_len dalam piksel; map ke power
        self.power = min(self.max_power, drag_len * 10)

    def reset(self):
        self.power = 0
        self.charging = False

    def shoot(self, cue_ball):
        # apply impulse ke cue ball berdasarkan aim_angle dan power
        if cue_ball.in_pocket:
            return
        px = cos(self.aim_angle) * self.power / cue_ball.mass
        py = sin(self.aim_angle) * self.power / cue_ball.mass
        cue_ball.vel = Vec2(px, py)
        # setelah ditembak, reset power
        self.reset()
