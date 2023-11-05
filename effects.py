import pygame as pg
import config

class Label(pg.sprite.Sprite):
    def __init__(self, text: str):
        pg.sprite.Sprite.__init__(self)

        self.fg = color.Color("black")
        self.bg =  color.Color("white")

        self.font = pg.freetype.SysFont(freetype.get_default_font(), 12)

        self.text = text
        self.image, self.rect = self.font.render(self.text, self.fg, self.bg)
    
    def update(self, parent: pg.sprite.Sprite =None):
        if parent:
            self.rect.x = parent.rect.x
            self.rect.y = parent.rect.y

        
class GameArea(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.rect.Rect(0,0, config.playFieldWidth, config.playFieldHeight)
        self.image = pg.surface.Surface((self.rect.width, self.rect.height))
        self.player = player
        if self.player == 0:
            pg.gfxdraw.rectangle(self.image, self.rect, pg.color.Color("red"))
        else:
            pg.gfxdraw.rectangle(self.image, self.rect, pg.color.Color("blue"))


