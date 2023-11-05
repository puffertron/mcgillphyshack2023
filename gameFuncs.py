import pygame as pg
import bodies
from missile import Missile
from state import State
import config
import math

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
            # targetx = mousepos.x + cls.clickDifference[0]
            # targety = mousepos.y + cls.clickDifference[1]

            cls.chosenPlanet.rect.x = mousepos.x + cls.clickDifference[0]
            cls.chosenPlanet.rect.y = mousepos.y + cls.clickDifference[1]
            
            #collision
            resolution = pg.Vector2()
            collisions = []
            bodyB = None
            bodyC = None
            for body in State.planetGroups[State.activePlayer]:
                if body == cls.chosenPlanet: continue
                if pg.sprite.collide_circle(cls.chosenPlanet, body):
                    normal = pg.Vector2(body.rect.center) - pg.Vector2(cls.chosenPlanet.rect.center)
                    collisions.append((body, normal))
                    resolution = (int(normal.length()) - (body.radius + cls.chosenPlanet.radius))* normal.normalize()
                    bodyB = body
                

            cls.chosenPlanet.rect.x += resolution.x
            cls.chosenPlanet.rect.y += resolution.y

            #double collission failsafe!
            #check collisions again 
            for body in State.planetGroups[State.activePlayer]:
                if body == cls.chosenPlanet or body == bodyB: continue
                if pg.sprite.collide_circle(cls.chosenPlanet, body):
                    bodyC = body
                    #get nono zone venn radii
                    radiusAB = cls.chosenPlanet.radius + bodyB.radius
                    radiusAC = cls.chosenPlanet.radius + bodyC.radius
                    
                    #check intersection points
                    point1, point2 = intersectTwoCircles(bodyB.rect.centerx, bodyB.rect.centery, radiusAB, 
                                        bodyC.rect.centerx, bodyC.rect.centery, radiusAC)
                    
                    dist1 = point1 - mousepos
                    dist2 = point2 - mousepos

                    #choose between the 2 points
                    if dist1.length() < dist2.length():
                        cls.chosenPlanet.rect.centerx = point1.x
                        cls.chosenPlanet.rect.centery = point1.y
                        
                    if dist1.length() > dist2.length():
                        cls.chosenPlanet.rect.centerx = point2.x
                        cls.chosenPlanet.rect.centery = point2.y

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
            distSquared = (cls.missile.rect.centerx - planet.rect.centerx)**2 + (cls.missile.rect.centery - planet.rect.centery)**2
            minDist = (planet.radius + cls.missile.radius)

            if distSquared <= minDist**2:
        
                #TODO collision stuff
                if planet in State.planetGroups[State.inactivePlayer]:
                    planet.kill()
                    print("killed enemy planet! with radius " + str(planet.radius))
                
                else:
                    print("hit an ally? with radius " + str(planet.radius))
                print(planet.groups())
                print(cls.missile.rect.center, planet.rect.center)
                print(distSquared, str(minDist**2))

                cls.missile.kill()
                cls.missile = None

                State.movingPlanetsMode = True
                State.missileLaunchedMode = False
                State.switchPlayer()
                break

                


def intersectTwoCircles(x1,y1,r1,x2,y2,r2):
    r1 = r1
    r2 = r2
    centerdx = x1 - x2
    centerdy = y1 - y2

    R = math.sqrt(centerdx * centerdx + centerdy * centerdy)
    R2 = R*R
    R4 = R2*R2
    a = (r1*r1 - r2*r2) / (2 * R2)
    r2r2 = (r1*r1 - r2*r2)
    c = math.sqrt(2 * (r1*r1 + r2*r2) / R2 - (r2r2 * r2r2) / R4 - 1)

    fx = (x1+x2) / 2 + a * (x2 - x1)
    gx = c * (y2 - y1) / 2
    ix1 = fx + gx
    ix2 = fx - gx

    fy = (y1+y2) / 2 + a * (y2 - y1)
    gy = c * (x1 - x2) / 2
    iy1 = fy + gy
    iy2 = fy - gy

    return (pg.Vector2(ix1, iy1), pg.Vector2(ix2, iy2))