import pygame as pg
from pygame import gfxdraw
from physics import Kinematics
from state import State

class Missile(pg.sprite.Sprite):
    def __init__(self, radius, initPos, initVel):
        pg.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pg.Surface((2 * self.radius, 2 * self.radius))
        self.rect = self.image.get_rect()

        #temp planet circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        gfxdraw.filled_circle(self.image, self.radius, self.radius, self.radius, (255,255,255))

        # Define a surface for effects
        self.effectsScreen = pg.surface.Surface((600, 800))
        self.effectsScreen.set_colorkey((0, 0, 0))

        # Kinematics Variables
        self.k = Kinematics(initPos, initVel)
        # self.k.pos = initPos
        # self.k.vel = initPos

        self.rect.center = self.k.pos

    def updateKinematics(self, planets):
        # returns a new kinematics object
        self.k.nextPosSIE(planets)
        self.rect.center = self.k.pos