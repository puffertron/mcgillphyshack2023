import pygame as pg
import bodies
from missile import Missile
from state import State
import config

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
            
                for planet in State.planetGroups[State.activePlayer]:
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
            for body in State.planetGroups[State.activePlayer]:
                if body == cls.chosenPlanet: continue
                if pg.sprite.collide_circle(cls.chosenPlanet, body):
                    normal = pg.Vector2(body.rect.center) - pg.Vector2(cls.chosenPlanet.rect.center)
                    resolution = (int(normal.length()) - (body.radius + cls.chosenPlanet.radius))* normal.normalize() 

            cls.chosenPlanet.rect.x += resolution.x
            cls.chosenPlanet.rect.y += resolution.y

            #Let go of mouse
            if not pg.mouse.get_pressed()[0]:
                cls.chosenPlanet = None
                State.movingPlanetsMode = False
                State.missileLaunchedMode = True

    missile: Missile = None
    @classmethod
    def missileLaunched(cls):
        """Called when in Shooting mode"""

        # Define our Missile and group it
        if cls.missile == None:
            cls.missile = Missile(config.missileRadius)
            State.playerGroups[State.activePlayer].add(cls.missile)

        # Determine acceleration based on position
        cls.missile.a = cls.missile.acceleleration()

        # Increment velocity based on a
        cls.missile.v += cls.missile.a

        # Increment position based on velocity
        cls.missile.oldX.append(cls.missile.oldX[-1] + cls.missile.v)
        cls.missile.rect.center = cls.missile.oldX[-1]

        # Only keep MaxLen old positions
        if len(cls.missile.oldX) > cls.missile.oldXMaxLen:
            cls.missile.oldX.pop(1)

        # Check if collision
        for planet in State.planets:
            distSquared = (cls.missile.rect.centerx - planet.rect.centerx)^2 + (cls.missile.rect.centery - planet.rect.centery)^2
            minDist = (planet.radius + cls.missile.radius)

            if distSquared <= minDist^2:
        
                #TODO collision stuff
                if planet in State.planetGroups[State.inactivePlayer]:
                    planet.kill()
                    print("killed enemy planet! with radius " + str(planet.radius))
                
                else:
                    print("hit an ally? with radius " + str(planet.radius))
                print(planet.groups())
                print(cls.missile.rect.center, planet.rect.center)
                print(distSquared, str(minDist^2))

                cls.missile.kill()
                cls.missile = None

                State.switchPlayer()
                break

                