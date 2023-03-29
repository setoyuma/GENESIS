import pygame as pg
from support import draw_text


class TextAnimation():
    def __init__(self, text, size, damage, location, color, duration, surf):
        self.text = text
        self.x = location[0]
        self.y = location[1]
        self.size = size
        self.damage = damage
        self.color = color
        self.duration = duration
        self.display_surface = surf
        self.frame_count = 0


    def draw(self):
        draw_text(self.display_surface, str(self.damage), (self.x, self.y), self.size, self.color, 0)


    def update(self):
        self.frame_count += 1
        self.draw()
        if self.frame_count > self.duration:
            return True