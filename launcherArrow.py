import pygame as pg
import config
from pygame import gfxdraw
import math

class launcherArrow(pg.sprite.Sprite):
    def __init__(self, activePlayer):
        pg.sprite.Sprite.__init__(self)
        
        self.radius = 4

        self.image = pg.Surface((self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()
        if activePlayer == 0:
            self.rect.center = (config.playFieldWidth/2, config.yposLauncher+10)
        elif activePlayer == 1:
            self.rect.center = (config.playFieldWidth/2, config.playFieldHeight- config.yposLauncher-10)
            #TODO - ,maybe flip sprite
        

        # temp Launcher circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        
        gfxdraw.circle(self.image, self.radius, self.radius, self.radius (255,0,0))

        self.picked = False