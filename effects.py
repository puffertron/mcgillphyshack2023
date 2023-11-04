import pygame
from pygame import Vector2
from pygame import freetype
from pygame import color


class Label(pygame.sprite.Sprite):
    def __init__(self, text: str, color, bg):
        pygame.sprite.Sprite.__init__(self)

        self.font = freetype.SysFont("Consolas", 12)

        self.text = text
        self.image, self.rect = self.font.render(self.text, True, color)
        bgimg = self.image
        bgimg.fill(bg)
        self.image = bgimg.blit(self.image,self.rect)

        
        
