import pygame
from pygame import Vector2
from pygame import freetype
from pygame import color


class Label(pygame.sprite.Sprite):
    def __init__(self, text: str):
        pygame.sprite.Sprite.__init__(self)

        self.fg = color.Color("black")
        self.bg =  color.Color("white")

        self.font = freetype.SysFont(freetype.get_default_font(), 12)

        self.text = text
        self.image, self.rect = self.font.render(self.text, self.fg, self.bg)
        # bgimg = self.image
        # bgimg.fill(bg)
        # bgimg.blit(self.image,self.rect)
        # self.image = bgimg
    
    def update(self, parent: pygame.sprite.Sprite =None):
        if parent:
            self.rect.x = parent.rect.x
            self.rect.y = parent.rect.y

        
     
