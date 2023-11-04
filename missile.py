import pygame
from pygame import Vector2
from pygame import gfxdraw
from physics import Kinematics

MISSILE_WIDTH, MISSILE_LENGTH = 10, 20

class Missile(pygame.sprite.Sprite):
    def __init__(self, initPos, initVel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((MISSILE_WIDTH, MISSILE_LENGTH))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))

        # Define a surface for effects
        self.effectsScreen = pygame.surface.Surface((600, 800))
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