import pygame as pg, sys
import random

class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.colors = ["red","green","blue","yellow","purple"]
    
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


    def addParticles(self, posX, posY):
        # adds particles
        # posX = pg.mouse.get_pos()[0]
        # posY = pg.mouse.get_pos()[1]
        radius = 6
        directionX = random.randint(-3,3)
        directionY = random.randint(-3,3)
        particleCircle = [[posX,posY], radius, [directionX, directionY]]
        self.particles.append(particleCircle)
    

    def deleteParticles(self):
        # remove particles after a certain time
        particleCopy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particleCopy

    