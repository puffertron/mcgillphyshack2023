import pygame as pg
import bodies
import missile
from state import State

class GameFuncs():
    """Funcs for different game modes, func will be called each frame"""


    clickDifference: tuple
    chosenPlanet: bodies.Planet = None
    @classmethod
    def movePlanet(cls):
        """Called when in Moving Planets Mode"""
        if not cls.chosenPlanet:
            #Check if clicking on planet
            if pg.mouse.get_pressed()[0]:
                mousepos = pg.Vector2(pg.mouse.get_pos())
                
                for planet in State.planets:
                    positionInMask = mousepos.x - planet.rect.x, mousepos.y - planet.rect.y
                    if planet.rect.collidepoint(mousepos) and planet.mask.get_at(positionInMask):
                        cls.chosenPlanet = planet
                        cls.clickDifference = (cls.chosenPlanet.rect.x - mousepos.x, cls.chosenPlanet.rect.y - mousepos.y)
                        break

        else: #planet is chosen
            mousepos = pg.Vector2(pg.mouse.get_pos())

            #Move planet
            cls.chosenPlanet.rect.x = mousepos.x + cls.clickDifference[0]
            cls.chosenPlanet.rect.y = mousepos.y + cls.clickDifference[1]


            # #drag n drop
            # mousepos = pg.Vector2(mouse.get_pos())
            # if mouse.get_pressed()[0]:
            #     if cls.chosenPlanet.rect.collidepoint(mousepos):
            #         #clicked!!
            #         cls.chosenPlanet.picked = True
            # else:
            #     cls.chosenPlanet.picked = False
            
            # if cls.chosenPlanet.picked:
            #     cls.chosenPlanet.rect.x = mousepos.x - cls.chosenPlanet.rect.width/2
            #     cls.chosenPlanet.rect.y = mousepos.y - cls.chosenPlanet.rect.height/2
            
            #collision
            resolution = pg.Vector2()
            collisions = []
            for body in State.planets:
                if body == cls.chosenPlanet: continue
                if pg.sprite.collide_circle(cls.chosenPlanet, body):
                    normal = pg.Vector2(body.rect.center) - pg.Vector2(cls.chosenPlanet.rect.center)
                    resolution = (int(normal.length()) - (body.radius + cls.chosenPlanet.radius))* normal.normalize() 

            cls.chosenPlanet.rect.x += resolution.x
            cls.chosenPlanet.rect.y += resolution.y

            if not pg.mouse.get_pressed()[0]:
                cls.chosenPlanet = None
                # TODO update state mode

    missile_: missile.Missile = None
    @classmethod
    def shootMissile(cls):
        """Called when in Shooting mode"""

        # Define our Missile and group it
        if cls.missile_ == None:
            cls.missile_ = missile.Missile()
            State.missleGroup.add(cls.missile_)

        # Determine acceleration based on position
        cls.missile_.a = cls.missile_.acceleleration(State.planets)

        # Increment velocity based on a
        cls.missile_.v += cls.missile_.a

        # Increment position based on velocity
        cls.missile_.oldX.append(cls.missile_.oldX[-1] + cls.missile_.v)
        cls.missile_.rect.center = cls.missile_.oldX[-1]

        # Only keep MaxLen old positions
        if len(cls.missile_.oldX) > cls.missile_.oldXMaxLen:
            cls.missile_.oldX.pop(1)