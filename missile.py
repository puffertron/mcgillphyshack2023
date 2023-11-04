import pygame
from pygame import gfxdraw

MISSILE_WIDTH, MISSILE_LENGTH = 10, 20

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((MISSILE_WIDTH, MISSILE_LENGTH))
        self.image.fill((255, 255, 255))

        