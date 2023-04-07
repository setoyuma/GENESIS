import pygame as pg
import random

from particle import ParticlePrinciple
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
        self.import_assets()
        self.rect = self.animation.animation[0].get_rect()
        self.rect.center = spawn_pos[0], spawn_pos[1]
        if not facing_right:
            self.speed *= -1
            self.animation.animation = [pg.transform.flip(image, True, False) for image in self.animation.animation]
        self.image = self.animation.update(0)
        self.particles = ParticlePrinciple()
    
    def import_assets(self):
        path = f'./assets/fireballs/{self.name}/'
        self.animation = []
        full_path = path
        original_images = import_folder(full_path)
        scaled_images = scale_images(original_images, (100, 40))
        self.animation = Animator(self.game, scaled_images, 0.05, loop=True)

    def update(self, dt, target):
        self.move(dt)

        # check if 50 ms has passed since projectile spawning
        self.frames_passed += 1
        if self.frames_passed >= 10:
            self.player.throwing_proj = False

        if self.speed > 0:
            x = self.rect.left
            start_angle, end_angle = (120, 220)
        else:
            x = self.rect.right
            start_angle, end_angle = (60, -60)
        y = self.rect.centery
        x += random.randint(-3, 3)
        y += random.randint(-3, 3)
        for i in range(5):
            if self.type == "EXFireball":
                self.particles.addParticles(x, y, "yellow", start_angle, end_angle)
            else:
                self.particles.addParticles(x, y, "white", start_angle, end_angle)

        # check projectile collision with opponent
        if self.rect.collidepoint(target.rect.centerx, target.rect.centery+10):
            if self.type == "LFireball":
                damage = 5
            elif self.type == "MFireball":
                damage = 7
            elif self.type == "HFireball":
                damage = 14
            elif self.type == "EXFireball":
                damage = 7 * 1.5

            self.player.projectile = None
            self.player.throwing_proj = False
            self.player.attack(target, damage)

    def move(self, dt):
        if self.type == "LFireball":
            self.rect.x += self.speed
        elif self.type == "MFireball":
            self.rect.x += int(self.speed * 1.5)
        elif self.type == "HFireball" or self.type == "EXFireball":
            self.rect.x += int(self.speed * 2.2)

        if self.rect.x < 0 or self.rect.x > self.game.settings["screen_width"]:
            self.projectile = None
            self.throwing_proj = False

        self.animation.update(dt)

    def draw(self, surf):
        if self.speed > 0:
            x = self.rect.left
        else:
            x = self.rect.right
        #pg.draw.rect(surf, (0,0,0), self.rect)
        surf.blit(self.image, self.rect.topleft)
        self.particles.emit()