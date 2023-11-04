import pygame
from pygame import Vector2
from pygame import gfxdraw
import effects
import random

class Planet(pygame.sprite.Sprite):
    def __init__(self, radius, mass, color):
        pygame.sprite.Sprite.__init__(self)

        self.radius = radius
        self.mass = mass
        self.color = color

        self.image = pygame.Surface((self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()

        #temp planet circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        gfxdraw.filled_circle(self.image, self.radius,self.radius,self.radius, self.color)

        self.picked = False

        self.children = pygame.sprite.Group()

        #debug stuff
        self.display_mass = False
        self.display_radius = False

    def debugDisplay(self):
        if self.display_mass:
            l = effects.Label(f"mass: {self.mass}", pygame.Color("white"), pygame.Color("orange"))
            self.children.add(l)
    
    def randomizePosition(self):
        self.rect.x = random.randint(0, 400)
        self.rect.y = random.randint(0, 400)

    def update(self, screen):
        self.children.update()
        self.children.draw(screen)
    
    def visualGravity(self):
        pass


