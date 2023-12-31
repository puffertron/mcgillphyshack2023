import pygame as pg
import config
from pygame import gfxdraw

# class Launcher2(pg.sprite.Sprite):
#     def __init__(self, activePlayer):
#         pg.sprite.Sprite.__init__(self)
#         self.image = pg.Surface((30,30))
#         self.image.fill((0,255,0))
#         self.rect = self.image.get_rect()
#         self.children = []


#         if activePlayer == 1:
#             self.rect.topleft = (config.windowWidth/2-self.rect.width/2, config.launchLine-self.rect.height/2)
#             # self.iLaunchRect.topleft = (config.windowWidth/2-lRad, config.launchLine-lRad)
#             # self.iArrowRect.topleft = (config.windowHeight/2-aRad, config.launchLine+aaRad/2)
#         elif activePlayer == 0:
#             self.image = pg.transform.rotate(self.image, 180)
#             # self.rect.bottomleft = (config.windowWidth/2-aaRad, config.windowHeight - (config.launchLine-lRad))
#             # self.iLaunchRect.bottomleft = (config.windowWidth/2-lRad, config.windowHeight - (config.launchLine-lRad))
#             # self.iArrowRect.bottomleft = (config.windowHeight/2-aRad, config.windowHeight - (config.launchLine+aaRad/2))

#     # def update(self):
#     #     mousepos = pg.Vector2(pg.mouse.get_pos)
#     #     if self.rect.collidepoint(mousepos):
#     #         if pg.mouse.get_pressed()[0]:
#     #             #click



class Launcher(pg.sprite.Sprite):
    def __init__(self, owner):
        pg.sprite.Sprite.__init__(self)
        self.speed = 0
        #aaRad = config.arrowAreaRadius
        lRad = config.launcherRadius
        #aRad = config.arrowheadRadius

        # Bounding boxes for whole setup, launcher ship, arrowhead
        self.image = pg.Surface((lRad*2, 2*lRad))

        #self.iLaunch = pg.Surface((lRad*2, lRad*2))

        #self.iArrow = pg.Surface((aRad*2, aRad*2))
        

        self.image.fill((255, 255, 255))
        self.image.set_colorkey((0,0,0))

        # self.iLaunch.fill((0, 100, 0))
        # self.iLaunch.set_colorkey((0,0,100))

        # self.iArrow.fill((0, 0, 100))
        # self.iArrow.set_colorkey((0,0,0))

        # gfxdraw.filled_circle(self.iLaunch, lRad, lRad, lRad, (255,255,255))

        # gfxdraw.filled_circle(self.iArrow, aRad, aRad, aRad, (255, 0, 0))

        # self.image.blit(self.iLaunch, pg.Rect(aaRad-lRad, 0, lRad*2, lRad*2))
        # self.image.blit(self.iArrow, pg.Rect(aaRad-aRad, aaRad/2+lRad-aRad, aRad*2, aRad*2))

        
        self.rect = self.image.get_rect()
        self.rect.y = config.windowHeight / 2 + config.playFieldHeight * (-1)**(owner)
        self.rect.x = config.windowWidth / 2
        #self.iLaunchRect = self.iLaunch.get_rect()
        #self.iArrowRect = self.iArrow.get_rect()


        # if activePlayer == 1:
        #     self.rect.topleft = (config.windowWidth/2-aaRad, config.launchLine-lRad)
        #     self.iLaunchRect.topleft = (config.windowWidth/2-lRad, config.launchLine-lRad)
        #     self.iArrowRect.topleft = (config.windowHeight/2-aRad, config.launchLine+aaRad/2)
        # elif activePlayer == 0:
        #     self.image = pg.transform.rotate(self.image, 180)
        #     self.rect.bottomleft = (config.windowWidth/2-aaRad, config.windowHeight - (config.launchLine-lRad))
        #     self.iLaunchRect.bottomleft = (config.windowWidth/2-lRad, config.windowHeight - (config.launchLine-lRad))
        #     self.iArrowRect.bottomleft = (config.windowHeight/2-aRad, config.windowHeight - (config.launchLine+aaRad/2))


        

        
        # gfxdraw.filled_circle(self.image, self.radius,self.radius,self.radius, (255,255,255))
        # gfxdraw.filled_circle(self.arrow, int(config.launchArrowRadius/2), int(config.launchArrowRadius/2 + (-1)**activePlayer*(self.radius*2)), 5, (255, 0, 0))

        # self.image.blit(self.arrow, pg.Rect(int(config.launchArrowRadius/2-self.radius), int(config.launchArrowRadius/2-self.radius), self.radius*2, self.radius*2) )

        # self.picked = False

        def getClickableArea():
            return 