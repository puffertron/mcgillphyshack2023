import pygame as pg
from pygame import gfxdraw
from state import State

class Missile(pg.sprite.Sprite):
    def __init__(self, radius):
        pg.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pg.Surface((2 * self.radius, 2 * self.radius))
        self.rect = self.image.get_rect()

        #temp planet circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        gfxdraw.filled_circle(self.image, self.radius, self.radius, self.radius, (255,255,255))

        # Define a surface for effects
        self.effectsScreen = pg.surface.Surface((600, 800))
        self.effectsScreen.set_colorkey((0, 0, 0))

        # Kinematics Variables
        self.v = pg.Vector2()
        self.a = pg.Vector2()
        self.oldX = [pg.Vector2(self.rect.center)]
        self.oldXMaxLen = 60

    def drawtrail(self, screen):
        # Reset the Screen
        self.effectsScreen.fill((0, 0, 0))
        
        # draw the trail across all saved past positions, decreasing opacity
        for i in range(-1, -1*len(self.oldX)+1, -1):
            alpha = round(255*(self.oldXMaxLen+i)/self.oldXMaxLen)
            gfxdraw.line(self.effectsScreen, int(self.oldX[i].x), int(self.oldX[i].y), int(self.oldX[i-1].x), int(self.oldX[i-1].y), (255, 255, 255, alpha))
        
        # Update the effects screen
        screen.blit(self.effectsScreen, self.effectsScreen.get_rect())


    def acceleleration(self):
        G = -1
        a = pg.Vector2() # empty acceleration
        xm = pg.Vector2(self.rect.center) # position of craft
        for p in State.planetGroups[State.activePlayer]:
            xp = pg.Vector2(p.rect.center) # position of planet

            # the contribution of each planet to the acceleration is
            # Mp * [ (x_diff) x^ + (y_diff) y^ ] / ||r_diff||^3
            a += p.mass*(xm - xp)/(((xm - xp).length())**3)

        # Multiply by our gravity  
        a *= G
        return a