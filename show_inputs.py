import pygame as pg
import sys

from support import get_image

class Arrow:
    def __init__(self, direction, x, y, size):
        self.display_surface = pg.display.get_surface()
        self.size = size
        self.image = get_image(f'./assets/input/arrows/{direction}.png')
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = pg.Rect(x, y, 80,80)
        self.x = x
        self.y = y

    def draw(self):
        self.display_surface.blit(self.image, (self.x, self.y))
        # pg.draw.rect(self.display_surface, "green", self.rect)


class User_Inputs:
    def __init__(self, x, y, size, player):
        self.display_surface = pg.display.get_surface()
        self.player = player
        self.rect = pg.Rect(x, y, 80,80)
        self.size = size
        self.x = x
        self.y = y
    
    def draw(self):
        match self.player.status:
            case "LP":
                self.image = get_image(f'./assets/ui/buttons/inputs/{self.player.status}.png')
                self.display_surface.blit(self.image, (self.x, self.y))
                # pg.draw.rect(self.display_surface, "green", self.rect)
            case "MP":
                self.image = get_image(f'./assets/ui/buttons/inputs/{self.player.status}.png')
                self.display_surface.blit(self.image, (self.x, self.y))
                # pg.draw.rect(self.display_surface, "green", self.rect)
            case "HP":
                self.image = get_image(f'./assets/ui/buttons/inputs/{self.player.status}.png')
                self.display_surface.blit(self.image, (self.x, self.y))
                # pg.draw.rect(self.display_surface, "green", self.rect)
            case "LK":
                self.image = get_image(f'./assets/ui/buttons/inputs/{self.player.status}.png')
                self.display_surface.blit(self.image, (self.x, self.y))
                # pg.draw.rect(self.display_surface, "green", self.rect)
            case "MK":
                self.image = get_image(f'./assets/ui/buttons/inputs/{self.player.status}.png')
                self.display_surface.blit(self.image, (self.x, self.y))
                # pg.draw.rect(self.display_surface, "green", self.rect)
            case "HK":
                self.image = get_image(f'./assets/ui/buttons/inputs/{self.player.status}.png')
                self.display_surface.blit(self.image, (self.x, self.y))
                # pg.draw.rect(self.display_surface, "green", self.rect)

        