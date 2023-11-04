import pygame as pg
import bodies
from missile import Missile
from state import State

class GameFuncs():
    """Funcs for different game modes, func will be called each frame"""


    clickDifference: tuple
    chosenPlanet: bodies.Planet = None
    @classmethod
    def movePlanet(cls):
        """Called when in Moving Planets Mode"""
        if not cls.chosenPlanet:
            #Check if starting to move planet
            if pg.mouse.get_pressed()[0]:
                mousepos = pg.Vector2(pg.mouse.get_pos())
                
                if State.currentPlayer == 0:
                    playersPlanets = State.p0Planets
                elif State.currentPlayer == 1:
                    playersPlanets = State.p1Planets

                for planet in playersPlanets:
                    #For each planet, see if clicking on planet
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

            #Let go of mouse
            if not pg.mouse.get_pressed()[0]:
                cls.chosenPlanet = None
                # TODO update state mode

    missile: Missile = None
    @classmethod
    def missileLaunched(cls):
        """Called when in Shooting mode"""

        # Define our Missile and group it
        if cls.missile == None:
            cls.missile = Missile()
            if State.currentPlayer == 0:
                State.addToP0Group(cls.missile)
            elif State.currentPlayer == 1:
                State.addToP1Group(cls.missile)
                

        # Determine acceleration based on position
        cls.missile.a = cls.missile.acceleleration(State.planets)

        # Increment velocity based on a
        cls.missile.v += cls.missile.a

        # Increment position based on velocity
        cls.missile.oldX.append(cls.missile.oldX[-1] + cls.missile.v)
        cls.missile.rect.center = cls.missile.oldX[-1]

        # Only keep MaxLen old positions
        if len(cls.missile.oldX) > cls.missile.oldXMaxLen:
            cls.missile.oldX.pop(1)