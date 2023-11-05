import pygame as pg
from pygame import gfxdraw
import effects
import random
import uuid

class Planet(pg.sprite.Sprite):
    def __init__(self, radius, mass, color, owner:int):
        pg.sprite.Sprite.__init__(self)

        self.radius = radius
        self.mass = mass
        self.color = color
        self.owner = owner

        self.image = pg.Surface((self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()

        #temp planet circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        gfxdraw.filled_circle(self.image, self.radius,self.radius,self.radius, self.color)

        self.picked = False

        self.children = pg.sprite.Group()

        #debug stuff
        self.display_mass = False
        self.display_radius = False

        #mask
        self.mask = pg.mask.from_surface(self.image)

    def debugDisplay(self):
        if self.display_mass:
            l = effects.Label(f"mass: {self.mass}")
            self.children.add(l)
    
    def randomizePosition(self, topleft, bottomright):
        self.rect.x = random.randint(topleft.x, bottomright.x)
        self.rect.y = random.randint(topleft.y, bottomright.y)

    def getInput(self):
        pass

    def update(self, screen):
        self.children.update(parent = self)
        self.children.draw(screen)


    def visualGravity(self):
        pass