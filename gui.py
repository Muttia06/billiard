# gui.py
"""
Keterangan singkat: Modul gui.py menggunakan pygame untuk menampilkan meja, bola, cue, dan power bar.
Catatan: UI dituliskan sederhana namun rapi; gunakan drag untuk aim & power.
"""
import pygame
from pygame import gfxdraw
from ball import Vec2

class GUI:
    def __init__(self, width=1000, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Simulasi Billiard - OOP & Encapsulation')
        self.font = pygame.font.SysFont('Arial', 16)

    def draw_table(self, table):
        # gambar background meja
        self.screen.fill((32, 80, 20))
        # lapisan hijau meja
        inner = pygame.Rect(table.left, table.top, table.width, table.height)
        pygame.draw.rect(self.screen, (30,120,50), inner)
        # gambar pockets
        for p in table.pockets:
            pygame.gfxdraw.filled_circle(self.screen, int(p[0]), int(p[1]), int(table.pocket_radius), (20,20,20))

    def draw_ball(self, ball):
        if ball.in_pocket:
            return
        pygame.gfxdraw.filled_circle(self.screen, int(ball.pos.x), int(ball.pos.y), int(ball.radius), ball.color)
        pygame.gfxdraw.aacircle(self.screen, int(ball.pos.x), int(ball.pos.y), int(ball.radius), (0,0,0))

    def draw_cue(self, cue, cue_ball):
        if cue_ball.in_pocket:
            return
        # gambar garis arah aim
        import math
        
    
    def draw_aim_line(self, cue_ball, cue, balls, table_rect):
        import math

        FIRST_LENGTH = 1000      # garis awal sebelum kena dinding
        BOUNCE_LENGTH = 20      # panjang garis setelah memantul

        ray_origin = Vec2(cue_ball.pos.x, cue_ball.pos.y)
        ray_dir = Vec2(math.cos(cue.aim_angle), math.sin(cue.aim_angle)).normalize()

        points = [(ray_origin.x, ray_origin.y)]

        # --- 1) BUAT GARIS PERTAMA — UNTIL KENA DINDING ---
        t_min = float("inf")
        hit_normal = None

        # kiri
        if ray_dir.x < 0:
            t = (table_rect.left - ray_origin.x) / ray_dir.x
            if 0 < t < t_min:
                t_min = t
                hit_normal = Vec2(1, 0)

        # kanan
        if ray_dir.x > 0:
            t = (table_rect.right - ray_origin.x) / ray_dir.x
            if 0 < t < t_min:
                t_min = t
                hit_normal = Vec2(-1, 0)

        # atas
        if ray_dir.y < 0:
            t = (table_rect.top - ray_origin.y) / ray_dir.y
            if 0 < t < t_min:
                t_min = t
                hit_normal = Vec2(0, 1)

        # bawah
        if ray_dir.y > 0:
            t = (table_rect.bottom - ray_origin.y) / ray_dir.y
            if 0 < t < t_min:
                t_min = t
                hit_normal = Vec2(0, -1)

        # titik tabrakan pertama
        first_hit = ray_origin + ray_dir * min(t_min, FIRST_LENGTH)
        points.append((first_hit.x, first_hit.y))

        # --- 2) SETELAH MENTUL, GARIS CUMA 20 PX ---
        # hitung arah pantulan
        if hit_normal is not None:
            bounce_dir = ray_dir - hit_normal * 2 * ray_dir.dot(hit_normal)
            bounce_dir = bounce_dir.normalize()

            # titik akhir segmen pantulan (20 px)
            bounce_end = first_hit + bounce_dir * BOUNCE_LENGTH
            points.append((bounce_end.x, bounce_end.y))

        

        # --- GAMBAR GARIS ---
        for i in range(len(points)-1):
            pygame.draw.line(self.screen, (255,255,200), points[i], points[i+1], 2)


    def draw_power_bar(self, cue):
        # tampilan bar power di bagian bawah
        bar_w = 300
        bar_h = 14
        x = (self.width - bar_w)//2
        y = self.height - 40
        pygame.draw.rect(self.screen, (60,60,60), (x,y,bar_w,bar_h))
        fill_w = int((cue.power / cue.max_power) * bar_w)
        pygame.draw.rect(self.screen, (200,50,50), (x,y,fill_w,bar_h))
        # teks
        text = self.font.render(f'Power: {int(cue.power)}', True, (255,255,255))
        self.screen.blit(text, (x, y - 20))

    def draw_scores(self, score_manager):
        x = 10
        y = 10
        for i,p in enumerate(score_manager.players):
            txt = f'{p.name}: {p.score}'
            surf = self.font.render(txt, True, (255,255,255))
            self.screen.blit(surf, (x, y + i*20))
        # highlight current
        cur = score_manager.current
        cur_txt = self.font.render(f"Giliran: {score_manager.players[cur].name}", True, (255,255,0))
        self.screen.blit(cur_txt, (self.width - 170, 10))

    def update(self):
        pygame.display.flip()
