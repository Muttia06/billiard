# game.py
"""
Keterangan singkat: Modul game.py mengorkestrasi semua komponen: inisialisasi, loop utama, input handling,
update physic, penanganan skor, dan restart ketika perlu.
"""
import pygame
from ball import Ball, Vec2
from physic import resolve_ball_collision, resolve_wall_collision, apply_friction, check_pocket
from table import Table
from cue import Cue
from score import Player, ScoreManager
from gui import GUI

class Game:
    def __init__(self):
        # buat meja dan GUI
        self.gui = GUI(1000,600)
        margin = 60
        self.table = Table(margin, margin, self.gui.width - margin, self.gui.height - margin - 60)
        # buat bola standard 9-ball layout contoh (sederhana)
        self.balls = []
        # cue ball
        self.cue_ball = Ball(0, Vec2(self.table.left + 120, (self.table.top + self.table.bottom)/2), radius=10, color=(255,255,255), is_cue=True)
        self.balls.append(self.cue_ball)
        # beberapa bola lain (dummy layout)
        colors = [(255,255,0),(0,0,255),(255,0,0),(128,0,128),(255,165,0),(0,128,0),(128,128,128),(0,0,0),(255,192,203)]
        for i in range(1,10):
            pos = Vec2(self.table.right - 160 + (i%2)*22, self.table.top + 150 + (i*18))
            self.balls.append(Ball(i, pos, radius=10, color=colors[(i-1)%len(colors)]))

        self.cue = Cue()
        self.players = [Player('P1'), Player('P2')]
        self.score = ScoreManager(self.players)

        # physics params
        self.friction = 60.0  # deceleration units

        self.clock = pygame.time.Clock()
        self.running = True
        self.mouse_down = False
        self.drag_start = None
        self.drag_end = None

    def all_balls_stopped(self):
        for b in self.balls:
            if not b.in_pocket and b.speed() > 1e-1:
                return False
        return True

    def update_physics(self, dt):
        # tumbukan bola-bola
        n = len(self.balls)
        for i in range(n):
            for j in range(i+1, n):
                resolve_ball_collision(self.balls[i], self.balls[j])
        # wall & friction & pocket
        for b in self.balls:
            resolve_wall_collision(b, self.table)
            check_pocket(b, self.table)
            apply_friction(b, self.friction, dt)
            b.update(dt)

    def handle_input(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                # jika klik dekat cue ball -> mulai drag untuk aim & power
                dx = mx - self.cue_ball.pos.x
                dy = my - self.cue_ball.pos.y
                if (dx*dx + dy*dy) <= (self.cue_ball.radius + 6)**2 and self.all_balls_stopped():
                    self.mouse_down = True
                    self.drag_start = Vec2(mx,my)
                    self.drag_end = Vec2(mx,my)
                    self.cue.charging = True
            elif ev.type == pygame.MOUSEBUTTONUP:
                if self.mouse_down and self.cue.charging:
                    # hit
                    drag_vec = Vec2(self.drag_start.x - self.drag_end.x, self.drag_start.y - self.drag_end.y)
                    drag_len = drag_vec.length()
                    if drag_len > 5:
                        # tentukan aim & power berdasarkan drag (tarik mundur lalu lepaskan)
                        self.cue.start_aim(self.cue_ball.pos, self.drag_end)
                        self.cue.set_power_by_drag(drag_len)
                        self.cue.shoot(self.cue_ball)
                    self.mouse_down = False
                    self.cue.charging = False
                    self.drag_start = None
                    self.drag_end = None
            elif ev.type == pygame.MOUSEMOTION:
                if self.mouse_down:
                    mx,my = pygame.mouse.get_pos()
                    self.drag_end = Vec2(mx,my)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_input()
            # jika sedang drag, update aim angle for visual
            if self.mouse_down and self.drag_start and self.drag_end:
                # aim dari cue ball ke drag_end
                self.cue.start_aim(self.cue_ball.pos, self.drag_end)
                drag_vec = Vec2(self.drag_start.x - self.drag_end.x, self.drag_start.y - self.drag_end.y)
                self.cue.set_power_by_drag(drag_vec.length())

            # update physics
            self.update_physics(dt)

            # scoring: jika ada bola baru masuk pocket, beri poin
            for b in self.balls:
                if b.in_pocket and not getattr(b, '_scored', False):
                    # tandai sudah dihitung
                    setattr(b, '_scored', True)
                    if b.is_cue:
                        # bola putih ke pocket: penalti, kembalikan bola
                        # return cue ball ke posisi awal center-left
                        b.set_in_pocket(False)
                        b.pos = Vec2(self.table.left + 120, (self.table.top + self.table.bottom)/2)
                        b.vel = Vec2(0,0)
                        # penalti: next player
                        self.score.next_player()
                    else:
                        # beri poin pemain saat ini
                        self.score.add_score(self.score.current, 1)

            # render
            self.gui.draw_table(self.table)
            for b in self.balls:
                self.gui.draw_ball(b)
            # cue only when all balls stopped
            if not self.cue_ball.in_pocket and self.all_balls_stopped():
                self.gui.draw_cue(self.cue, self.cue_ball)
                self.gui.draw_aim_line(self.cue_ball, self.cue, self.balls, pygame.Rect(self.table.left, self.table.top, self.table.width, self.table.height))
            self.gui.draw_power_bar(self.cue)
            self.gui.draw_scores(self.score)
            self.gui.update()

        pygame.quit()
