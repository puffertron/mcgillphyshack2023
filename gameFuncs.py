import pygame as pg
import bodies
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

            if not pg.mouse.get_pressed()[0]:
                cls.chosenPlanet = None
                # TODO update state mode