import pygame as pg
import random
import math
import sys

from support import import_folder, scale_images

class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.animation_speed = 0.25
        self.size = 64
        self.frame_index = 0
        self.import_assets()
        self.image = self.animation[self.frame_index]
        self.color = "red"

    def emit(self):
        # move/draw particles
        if self.particles:
            self.deleteParticles()
            for particle in self.particles:
                #move particle
                particle[0][1] += particle[2][1]
                particle[0][0] += particle[2][0]
                #shrink particle
                particle[1] -= 0.2
                #draw circle around particle
                pg.draw.circle(pg.display.get_surface(), pg.Color(particle[3]), particle[0], int(particle[1]))
                # pg.draw.circle(pg.display.get_surface(),pg.Color(random.choice(self.colors)),particle[0], int(particle[1]))
                # pg.draw.circle(pg.display.get_surface(),pg.Color(random.choice(self.colors)),particle[0], int(particle[1]))

    def import_assets(self):
        path = f'./assets/vfx/hit/'
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

    def random_direction(self, start_angle_degrees, end_angle_degrees):
        angle_degrees = random.uniform(start_angle_degrees, end_angle_degrees)
        angle_radians = math.radians(angle_degrees)
        dx = math.cos(angle_radians) * random.randint(0,3)
        dy = math.sin(angle_radians) * random.randint(0,3)
        return dx, dy

    def addParticles(self, posX, posY, color="red", start_angle=None, end_angle=None, radius=6):
        self.posX = posX
        self.posY = posY
        if start_angle is None:
            directionX = random.randint(-3,3)
            directionY = random.randint(-3,3)
        else:
            directionX, directionY = self.random_direction(start_angle, end_angle)
        particleCircle = [[posX,posY], radius, [directionX, directionY], color]
        self.particles.append(particleCircle)

    def draw(self):
        pg.display.get_surface().blit(self.image, (self.posX, self.posY))

    def update(self):
        #anim
        self.animate()
        self.draw()

    def deleteParticles(self):
        # remove particles after a certain time
        particleCopy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particleCopy