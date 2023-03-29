import pygame as pg, sys
import random

from support import import_folder, scale_images

class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.colors = ["red","green","blue","yellow","purple"]
        self.animation_speed = 0.25
        self.size = 64
        self.frame_index = 0
        self.import_assets()
        self.image = self.animation[self.frame_index]
    
    def emit(self, color):
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
                pg.draw.circle(pg.display.get_surface(),pg.Color(color),particle[0], int(particle[1]))
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

    def addParticles(self, posX, posY):
        # adds particles
        # posX = pg.mouse.get_pos()[0]
        # posY = pg.mouse.get_pos()[1]
        self.posX = posX
        self.posY = posY
        radius = 6
        directionX = random.randint(-3,3)
        directionY = random.randint(-3,3)
        particleCircle = [[posX,posY], radius, [directionX, directionY]]
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

    