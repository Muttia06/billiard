# ball.py
"""
Keterangan singkat: Modul ball.py berisi kelas Ball yang merepresentasikan bola pada meja.
- Encapsulation: atribut-atribut sensitif (kecepatan, posisi, radius) dilindungi.
- Inheritance & Polymorphism: kalau mau membuat jenis bola lain (mis. cue ball) bisa mewarisi Ball.
"""
from dataclasses import dataclass
import math

@dataclass
class Vec2:
    x: float
    y: float

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float):
        return Vec2(self.x * k, self.y * k)

    def __rmul__(self, k: float):
        return self.__mul__(k)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        l = self.length()
        if l == 0:
            return Vec2(0,0)
        return Vec2(self.x / l, self.y / l)

class Ball:
    def __init__(self, id_, pos: Vec2, radius=10, mass=1.0, color=(255,255,255), is_cue=False):
        # encapsulated attributes
        self._id = id_
        self._pos = pos
        self._vel = Vec2(0.0, 0.0)
        self._radius = radius
        self._mass = mass
        self._color = color
        self._in_pocket = False
        self.is_cue = is_cue

    # property untuk akses terkontrol
    @property
    def id(self):
        return self._id

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, v: Vec2):
        self._pos = v

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, v: Vec2):
        self._vel = v

    @property
    def radius(self):
        return self._radius

    @property
    def mass(self):
        return self._mass

    @property
    def color(self):
        return self._color

    @property
    def in_pocket(self):
        return self._in_pocket

    def set_in_pocket(self, val: bool):
        # method terkontrol untuk mengubah status pocket
        self._in_pocket = val
        if val:
            # saat masuk pocket, hentikan kecepatan
            self._vel = Vec2(0,0)

    def speed(self):
        return self._vel.length()

    def update(self, dt):
        # perbarui posisi berdasarkan velocity (integrasi sederhana)
        if not self._in_pocket:
            self._pos = Vec2(self._pos.x + self._vel.x * dt, self._pos.y + self._vel.y * dt)
