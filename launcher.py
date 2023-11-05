import pygame as pg
import config
from pygame import gfxdraw

class Launcher(pg.sprite.Sprite):
    def __init__(self, activePlayer):
        pg.sprite.Sprite.__init__(self)

        self.radius = 10

        self.image = pg.Surface((self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()
        if activePlayer == 0:
            self.rect.center = (config.playFieldWidth/2, config.yposLauncher)
        elif activePlayer == 1:
            self.rect.center = (config.playFieldWidth/2, config.playFieldHeight- config.yposLauncher)
            #TODO - ,maybe flip sprite
        

        # temp Launcher circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        gfxdraw.filled_circle(self.image, self.radius,self.radius,self.radius, (255,255,255))

        self.picked = False