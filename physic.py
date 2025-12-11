# physic.py
"""
Keterangan singkat: Modul physic.py menangani tumbukan antar bola, tumbukan ke dinding,
friction, dan deteksi pocket. Semua fungsi diletakkan terpisah untuk single responsibility.
"""
import math
from ball import Vec2

def resolve_ball_collision(b1, b2):
    # jika salah satu di pocket, tidak diproses
    if b1.in_pocket or b2.in_pocket:
        return
    dp = b1.pos - b2.pos
    dist = dp.length()
    if dist == 0:
        # very small jitter: sedikit geser
        dist = 0.001
        dp = Vec2(0.001,0)
    overlap = b1.radius + b2.radius - dist
    if overlap > 0:
        # geser bola supaya tidak overlap (positional correction)
        correction = dp.normalize() * (overlap/2 + 1e-6)
        b1.pos = b1.pos + correction
        b2.pos = b2.pos - correction

        # compute relative velocity along normal
        normal = dp.normalize()
        rel_vel = b1.vel - b2.vel
        vel_along_normal = rel_vel.dot(normal)
        if vel_along_normal > 0:
            return
        # restitution (elasticity)
        e = 0.75
        j = -(1 + e) * vel_along_normal
        j /= (1/b1.mass + 1/b2.mass)
        impulse = normal * j
        b1.vel = b1.vel + impulse * (1 / b1.mass)
        b2.vel = b2.vel - impulse * (1 / b2.mass)

def resolve_wall_collision(ball, table):
    if ball.in_pocket:
        return
    r = ball.radius
    # meja dimensi: table.left, table.top, table.right, table.bottom
    if ball.pos.x - r < table.left:
        ball.pos = Vec2(table.left + r, ball.pos.y)
        ball.vel = Vec2(-ball.vel.x * table.wall_restitution, ball.vel.y)
    if ball.pos.x + r > table.right:
        ball.pos = Vec2(table.right - r, ball.pos.y)
        ball.vel = Vec2(-ball.vel.x * table.wall_restitution, ball.vel.y)
    if ball.pos.y - r < table.top:
        ball.pos = Vec2(ball.pos.x, table.top + r)
        ball.vel = Vec2(ball.vel.x, -ball.vel.y * table.wall_restitution)
    if ball.pos.y + r > table.bottom:
        ball.pos = Vec2(ball.pos.x, table.bottom - r)
        ball.vel = Vec2(ball.vel.x, -ball.vel.y * table.wall_restitution)

def apply_friction(ball, mu, dt):
    if ball.in_pocket:
        return
    speed = ball.speed()
    if speed == 0:
        return
    # friction deceleration
    dec = mu * dt
    new_speed = max(0, speed - dec)
    if new_speed == 0:
        ball.vel = Vec2(0,0)
    else:
        ball.vel = ball.vel * (new_speed / speed)

def check_pocket(ball, table):
    if ball.in_pocket:
        return False
    for p in table.pockets:
        dx = ball.pos.x - p[0]
        dy = ball.pos.y - p[1]
        if math.hypot(dx, dy) <= table.pocket_radius:
            ball.set_in_pocket(True)
            return True
    return False
