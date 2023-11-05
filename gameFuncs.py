import pygame as pg
from pygame import Vector2
import bodies
from missile import Missile
from launcher import Launcher
from state import State
import config
import math
import time

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
                        
            cls.chosenPlanet.rect.clamp_ip(State.playrects[cls.chosenPlanet.owner])

            if not pg.mouse.get_pressed()[0]:
                cls.chosenPlanet = None
                State.movingPlanetsMode = False
                State.missileLaunchedMode = True

    clickDifference: tuple
    movingLauncher: bool = False
    @classmethod
    def controlLauncher(cls):
        """Called when in Control Launcher Mode"""
        if not cls.movingLauncher:
            #Check if starting to move launcher
            if pg.mouse.get_pressed()[0]:
                mousepos = pg.Vector2(pg.mouse.get_pos())
            
                if State.launcher.rect.collidepoint(mousepos):
                    cls.movingLauncher = True
                    cls.clickDifference = (State.launcher.rect.x - mousepos.x, State.launcher.rect.y - mousepos.y)
                
        else: #launcher is moving
            mousepos = pg.Vector2(pg.mouse.get_pos())

            State.launcher.rect.x = mousepos.x + cls.clickDifference[0]

            if not pg.mouse.get_pressed()[0]:
                cls.movingLauncher = False

    marker: pg.sprite.Sprite = None
    missile: Missile = None
    leftBoundsTime = 0
    launchedTime = 0
    @classmethod
    def missileLaunched(cls):
        """Called when in Shooting mode"""

        print(cls.missile)
        # Define our Missile and group it
        if cls.missile == None:
            cls.missile = Missile(config.missileRadius, Vector2(), Vector2())
            State.playerGroups[State.activePlayer].add(cls.missile)
            cls.launchedTime = time.time()

        if time.time() - cls.launchedTime > 20:
            print("switched due to timeout")
            cls.missile.kill()
            cls.missile = None

            State.movingPlanetsMode = True
            State.missileLaunchedMode = False
            State.switchPlayer()
            return

        # Update Missile Position
        cls.missile.updateKinematics(State.planets)

        # Check if out of bounds
        bounds = pg.Rect(((config.windowWidth - config.playFieldWidth) / 2, (config.windowHeight - 2*config.playFieldHeight) / 2, config.playFieldWidth, 2*config.playFieldHeight))
        if not bounds.collidepoint(cls.missile.rect.center):
            if cls.marker == None:
                cls.marker = pg.sprite.Sprite(State.playerGroups[State.activePlayer])
                cls.marker.image = pg.Surface((config.markerSize, config.markerSize))
                cls.marker.image.fill("white")
                cls.marker.rect = cls.marker.image.get_rect()

                cls.leftBoundsTime = time.time()

            if time.time() - cls.leftBoundsTime > 5:
                print("switched due to out of bounds")
                cls.marker.kill()
                cls.marker = None

                cls.missile.kill()
                cls.missile = None

                State.movingPlanetsMode = True
                State.missileLaunchedMode = False
                State.switchPlayer()
                return

            # x position of marker
            if (bounds.left <= cls.missile.rect.centerx and cls.missile.rect.centerx <= bounds.right):
                marker_x = cls.missile.rect.centerx - config.markerSize / 2
            else:
                x_direction = (bounds.left - cls.missile.rect.centerx) / abs(bounds.left - cls.missile.rect.centerx)
                marker_x = bounds.centerx - (bounds.width / 2) * x_direction - config.markerSize / 2

            # y position of marker
            if (bounds.top <= cls.missile.rect.centery and cls.missile.rect.centery <= bounds.bottom):
                marker_y = cls.missile.rect.centery - config.markerSize / 2
            else:
                y_direction = (bounds.left - cls.missile.rect.centery) / abs(bounds.left - cls.missile.rect.centery)
                marker_y = bounds.centery - (bounds.height / 2) * y_direction - config.markerSize / 2

            # set marker position
            cls.marker.rect.x = marker_x
            cls.marker.rect.y = marker_y

        elif not cls.marker == None:
            cls.marker.kill()
            cls.marker = None


        # Check if collision
        for planet in State.planets:
            distSquared = (cls.missile.rect.centerx - planet.rect.centerx)**2 + (cls.missile.rect.centery - planet.rect.centery)**2
            minDist = (planet.radius + cls.missile.radius)

            if distSquared <= minDist**2:
                print("switched due to collision")
                #TODO collision stuff
                if planet in State.planetGroups[State.inactivePlayer]:
                    planet.kill()
                    print("killed enemy planet! with radius " + str(planet.radius))

                cls.missile.kill()
                cls.missile = None

                State.movingPlanetsMode = True
                State.missileLaunchedMode = False
                State.switchPlayer()
                return

                


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