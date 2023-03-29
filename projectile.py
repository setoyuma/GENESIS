import pygame as pg
from support import *

class Projectile():
    def __init__(self, name, type, size, spawn_pos, player, facing_right):
        # self.image = anim_list[0]
        self.name = name
        self.type = type
        self.size = size
        self.player = player
        self.speed = 10
        self.animation_speed = 0.25
        self.frame_index = 0
        self.frames_passed = 0
        self.import_assets()
        self.rect = pg.Rect(spawn_pos[0], spawn_pos[1], self.size, self.size)
        if not facing_right:
            self.speed *= -1
            self.animation = [pg.transform.flip(image, True, False) for image in self.animation]
    def import_assets(self):
        path = f'./assets/fireballs/{self.name}/'
        self.animation = []
        full_path = path
        original_images = import_folder(full_path)
        scaled_images = scale_images(original_images, (self.size, self.size))
        self.animation = scaled_images

    def animate(self):
		# loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]
        self.frame_index += 1

    def move(self):
        if self.type == "LFB":
            self.rect.x += self.speed
        if self.type == "MFB":
            self.rect.x += int(self.speed * 1.5)
        if self.type == "HFB":
            self.rect.x += int(self.speed * 2.2)

    def draw(self, surf):
        self.animate()
        surf.blit(self.image, (self.rect.x, self.rect.y))