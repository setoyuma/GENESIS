import pygame as pg

from animation import Animator
from support import *

class Projectile:
    def __init__(self, name, type, size, spawn_pos, player, facing_right, game):
        self.name = name
        self.type = type
        self.size = size
        self.player = player
        self.game = game
        self.speed = 10
        self.frame_index = 0
        self.frames_passed = 0
        self.off_screen = False
        self.import_assets()
        self.rect = pg.Rect(spawn_pos[0], spawn_pos[1], self.size, self.size)
        if not facing_right:
            self.speed *= -1
            self.animation.animation = [pg.transform.flip(image, True, False) for image in self.animation.animation]
        self.image = self.animation.update(0)
    
    def import_assets(self):
        path = f'./assets/fireballs/{self.name}/'
        self.animation = []
        full_path = path
        original_images = import_folder(full_path)
        scaled_images = scale_images(original_images, (100, 40))
        self.animation = Animator(self.game, scaled_images, 0.05, loop=True)

    def move(self):
        if self.type == "LFB":
            self.rect.x += self.speed
        elif self.type == "MFB":
            self.rect.x += int(self.speed * 1.5)
        elif self.type == "HFB":
            self.rect.x += int(self.speed * 2.2)

        if self.rect.x < 0 or self.rect.x > self.game.settings["screen_width"]:
            self.off_screen = True

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))