import pygame as pg
import config
import assets

def blit_mask(source, dest, destpos, mask, maskrect):
    """
    Blit an source image to the dest surface, at destpos, with a mask, using
    only the maskrect part of the mask.
    """
    tmp = source.copy()
    tmp.blit(mask, maskrect.topleft, maskrect, special_flags=pg.BLEND_RGBA_MULT)
    dest.blit(tmp, destpos, dest.get_rect().clip(maskrect))

def scrollX(screenSurf, offsetX):
    width, height = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (offsetX, 0))
    if offsetX < 0:
        screenSurf.blit(copySurf, (width + offsetX, 0), (0, 0, -offsetX, height))
    else:
        screenSurf.blit(copySurf, (0, 0), (width - offsetX, 0, offsetX, height))

def scrollY(screenSurf, offsetY):
    width, height = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (0, offsetY))
    if offsetY < 0:
        screenSurf.blit(copySurf, (0, height + offsetY), (0, 0, width, -offsetY))
    else:
        screenSurf.blit(copySurf, (0, 0), (0, height - offsetY, width, offsetY))

def realScroll(screensurf, x, y):
    scrollX(screensurf, x)
    scrollY(screensurf, y)

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

        
class GameArea(pg.sprite.DirtySprite):
    def __init__(self, player):
        pg.sprite.DirtySprite.__init__(self)
        self.rect = pg.rect.Rect(0,0, config.playFieldWidth, config.playFieldHeight)
        self.image = pg.surface.Surface((self.rect.width, self.rect.height))
        art = assets.UI_ELEMENTS[2]
        art = pg.transform.smoothscale(art, self.image.get_rect().size)
        self.image = art
        # self.image.set_alpha(100)
        self.player = player
        # if self.player == 0:
        #     pg.gfxdraw.rectangle(self.image, self.rect, pg.color.Color("red"))
        # else:
        #     pg.gfxdraw.rectangle(self.image, self.rect, pg.color.Color("blue"))



class ScrollSprite(pg.sprite.DirtySprite):
    def __init__(self, speed=2):
        pg.sprite.DirtySprite.__init__(self)
        self.scrolltexture: pg.Surface
        self.scrollspeed = speed
        self.mask: pg.Surface
        

    def update(self):
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))

        realScroll(self.scrolltexture, self.scrollspeed, -self.scrollspeed)
        self.scrolltexture = pg.transform.smoothscale(self.scrolltexture, (config.windowWidth, config.windowHeight))
        r = self.image.get_rect()
        blit_mask(self.scrolltexture, self.image, r, self.mask, self.image.get_rect())
        self.rect = self.image.get_rect()
        

class GlobalEffects(pg.sprite.DirtySprite):
    def __init__(self, blendmode=0):
        pg.sprite.DirtySprite().__init__(self)
        self.blendmode = blendmode
        self.image = pg.Surface((config.windowWidth, config.windowHeight))
        self.rect = self.image.get_rect()
        self.layers = []
        self.layers.append(pg.Surface((config.windowWidth, config.windowHeight)))
    
    def composite(self):
        for layer in self.layers:
            self.image.blit(self.layers[i], self.rect)
    
    def newlayer(self):
        new = pg.Surface((config.windowWidth, config.windowHeight))
        self.layers.append(new)
        return new
    
    def update(self):
        for layer in self.layers:
            layer.fill((0,0,0))
            layer.set_colorkey((0,0,0))

