# score.py
"""
Keterangan singkat: Modul score.py menyimpan data pemain dan skor.
"""
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class ScoreManager:
    def __init__(self, players):
        self.players = players
        self.current = 0

    def add_score(self, player_idx, points):
        self.players[player_idx].score += points

    def next_player(self):
        self.current = (self.current + 1) % len(self.players)
