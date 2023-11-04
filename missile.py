import pygame
from pygame import Vector2
from pygame import gfxdraw

MISSILE_WIDTH, MISSILE_LENGTH = 10, 20

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((MISSILE_WIDTH, MISSILE_LENGTH))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))

        # Define a surface for effects
        self.effectsScreen = pygame.surface.Surface((600, 800))
        self.effectsScreen.set_colorkey((0, 0, 0))

        # Kinematics Variables
        self.v = Vector2()
        self.a = Vector2()
        self.oldX = [Vector2(self.rect.center)]
        self.oldXMaxLen = 60

    #def update(self, planets, screen):
        
        # Determine acceleration based on position
        #self.a = self.acceleleration(planets)

        # Increment velocity based on a
        #self.v = self.v + self.a

        # Increment position based on velocity
        #self.oldX.append(self.oldX[-1] + self.v)
        #self.rect.center = self.oldX[-1]

        # Only keep MaxLen old positions
        #if len(self.oldX) > self.oldXMaxLen:
        #    self.oldX.pop(1)

        # Draw the tail
        #self.drawtrail(screen)

    def drawtrail(self, screen):
        # Reset the Screen
        self.effectsScreen.fill((0, 0, 0))
        
        # draw the trail across all saved past positions, decreasing opacity
        for i in range(-1, -1*len(self.oldX)+1, -1):
            alpha = round(255*(self.oldXMaxLen+i)/self.oldXMaxLen)
            gfxdraw.line(self.effectsScreen, int(self.oldX[i].x), int(self.oldX[i].y), int(self.oldX[i-1].x), int(self.oldX[i-1].y), (255, 255, 255, alpha))
        
        # Update the effects screen
        screen.blit(self.effectsScreen, self.effectsScreen.get_rect())


    def acceleleration(self, planets):
        G = -1
        a = Vector2() # empty acceleration
        xm = Vector2(self.rect.center) # position of craft
        for p in planets:
            xp = Vector2(p.rect.center) # position of planet

            # the contribution of each planet to the acceleration is
            # Mp * [ (x_diff) x^ + (y_diff) y^ ] / ||r_diff||^3
            a += p.mass*(xm - xp)/(((xm - xp).length())**3)

        # Multiply by our gravity  
        a *= G
        return a