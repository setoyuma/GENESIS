import pygame as pg, sys
# from settings import *

class Arrow:
    def __init__(self, direction, x, y, size):
        self.display_surface = pg.display.get_surface()
        self.size = size
        self.image = pg.image.load(f'./assets/input/arrows/{direction}.png')
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = pg.Rect(x, y, 80,80)
        self.x = x
        self.y = y

    def update(self):
        self.display_surface.blit(self.image, (self.x, self.y))
        # pg.draw.rect(self.display_surface, "green", self.rect)

