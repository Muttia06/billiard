# table.py
"""
Keterangan singkat: Modul table.py membuat objek meja yang menyimpan dimensi, posisi pocket,
dan aturan seperti restitusi dinding.
"""
class Table:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.width = right - left
        self.height = bottom - top
        # tentukan 6 pocket pada meja standar
        self.pocket_radius = 20
        self.pockets = [
            (left, top),
            ((left+right)/2, top),
            (right, top),
            (left, bottom),
            ((left+right)/2, bottom),
            (right, bottom)
        ]
        self.wall_restitution = 0.75
