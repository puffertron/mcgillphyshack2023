import pygame as pg
from pygame import gfxdraw
import effects
import random
import uuid

class Planet(pg.sprite.Sprite):
    def __init__(self, radius, mass, color):
        pg.sprite.Sprite.__init__(self)

        self.radius = radius
        self.mass = mass
        self.color = color

        self.image = pg.Surface((self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()

        #temp planet circle
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        gfxdraw.filled_circle(self.image, self.radius,self.radius,self.radius, self.color)

        self.picked = False

        self.children = pg.sprite.Group()

        #debug stuff
        self.display_mass = False
        self.display_radius = False

        #mask
        self.mask = pg.mask.from_surface(self.image)

    def debugDisplay(self):
        if self.display_mass:
            l = effects.Label(f"mass: {self.mass}")
            self.children.add(l)
    
    def randomizePosition(self):
        self.rect.x = random.randint(0, 200)
        self.rect.y = random.randint(0, 200)

    def getInput(self):
        pass

    def update(self, screen):
        self.children.update(parent = self)
        self.children.draw(screen)
        

        #drag n drop
        mousepos = Vector2(mouse.get_pos())
        if mouse.get_pressed()[0]:
            if self.rect.collidepoint(mousepos):
                #clicked!!
                self.picked = True
        else:
            self.picked = False
        
        if self.picked:
            self.rect.x = mousepos.x - self.rect.width/2
            self.rect.y = mousepos.y - self.rect.height/2
        
            #collision
            target_group = self.groups()[0]

            resolution = Vector2()
            collisions = []
            for body in target_group:
                if body == self: continue
                if pygame.sprite.collide_circle(self, body):
                    normal = Vector2(body.rect.center) - Vector2(self.rect.center)
                    collisions.append((body, normal))

                    normal = Vector2(body.rect.center) - Vector2(self.rect.center)
                    resolution = (int(normal.length()) - (body.radius + self.radius))* normal.normalize() 
                    print(f"r1:{body.radius} r2:{self.radius}")        
            
            self.rect.x += resolution.x
            self.rect.y += resolution.y


    
    def visualGravity(self):
        pass