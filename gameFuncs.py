import pygame as pg
from pygame import Vector2
from pygame import gfxdraw
import bodies
from missile import Missile
from launcher import Launcher
from state import State
import config
import math
import ui
import time

class GameFuncs():
    """Funcs for different game modes, func will be called each frame"""


    clickDifference: tuple
    planetActivelyMoving:bool = False
    # chosenPlanet: bodies.Planet = None   #Now in State
    @classmethod
    def movePlanet(cls):
        """Called when in Moving Planets Mode"""
        if not State.chosenPlanet or not cls.planetActivelyMoving: #If haven't clicked on planet yet or let go of active planet, check if click on it
            #Check if starting to move planet
            if pg.mouse.get_pressed()[0]:
                mousepos = pg.Vector2(pg.mouse.get_pos())
                flippedMousePos = pg.Vector2(
                        (mousepos.x - config.windowWidth / 2) * (-1)**(State.activePlayer) + config.windowWidth / 2,
                        (mousepos.y - config.windowHeight / 2) * (-1)**(State.activePlayer) + config.windowHeight / 2
                    )

                if State.chosenPlanet == None:
                    planetsToCheck = State.planetGroups[State.activePlayer] #Can click on any planet if none chosen yet
                else:
                    planetsToCheck = [State.chosenPlanet] #Can only click on chosen planet

                for planet in planetsToCheck:
                    #For each planet, see if clicking on planet
                    positionInMask = flippedMousePos.x - planet.rect.x, flippedMousePos.y - planet.rect.y
                    if planet.rect.collidepoint(flippedMousePos) and planet.mask.get_at(positionInMask):
                        State.chosenPlanet = planet
                        cls.planetActivelyMoving = True
                        cls.clickDifference = (State.chosenPlanet.rect.x - flippedMousePos.x, State.chosenPlanet.rect.y - flippedMousePos.y)
                        break

        else: #planet is chosen and moving
            mousepos = pg.Vector2(pg.mouse.get_pos())
            flippedMousePos = pg.Vector2(
                        (mousepos.x - config.windowWidth / 2) * (-1)**(State.activePlayer) + config.windowWidth / 2,
                        (mousepos.y - config.windowHeight / 2) * (-1)**(State.activePlayer) + config.windowHeight / 2
                    )

            #Move planet
            # targetx = mousepos.x + cls.clickDifference[0]
            # targety = mousepos.y + cls.clickDifference[1]

            State.chosenPlanet.rect.x = flippedMousePos.x + cls.clickDifference[0]
            State.chosenPlanet.rect.y = flippedMousePos.y + cls.clickDifference[1]
            
            #collision
            resolution = pg.Vector2()
            collisions = []
            bodyB = None
            bodyC = None
            for body in State.planetGroups[State.activePlayer]:
                if body == State.chosenPlanet: continue
                if pg.sprite.collide_circle(State.chosenPlanet, body):
                    normal = pg.Vector2(body.rect.center) - pg.Vector2(State.chosenPlanet.rect.center)
                    collisions.append((body, normal))
                    # if normal.length():
                    resolution = (int(normal.length()) - (body.radius + State.chosenPlanet.radius))* normal.normalize()
                    bodyB = body
                

            State.chosenPlanet.rect.x += resolution.x
            State.chosenPlanet.rect.y += resolution.y

            #double collission failsafe!
            #check collisions again 
            for body in State.planetGroups[State.activePlayer]:
                if body == State.chosenPlanet or body == bodyB: continue
                if pg.sprite.collide_circle(State.chosenPlanet, body):
                    bodyC = body
                    #get nono zone venn radii
                    radiusAB = State.chosenPlanet.radius + bodyB.radius
                    radiusAC = State.chosenPlanet.radius + bodyC.radius
                    
                    #check intersection points
                    point1, point2 = intersectTwoCircles(bodyB.rect.centerx, bodyB.rect.centery, radiusAB, 
                                        bodyC.rect.centerx, bodyC.rect.centery, radiusAC)
                    
                    dist1 = point1 - flippedMousePos
                    dist2 = point2 - flippedMousePos

                    #choose between the 2 points
                    if dist1.length() < dist2.length():
                        State.chosenPlanet.rect.centerx = point1.x
                        State.chosenPlanet.rect.centery = point1.y
                        
                    if dist1.length() > dist2.length():
                        State.chosenPlanet.rect.centerx = point2.x
                        State.chosenPlanet.rect.centery = point2.y
                        
            State.chosenPlanet.rect.clamp_ip(State.playrects[State.chosenPlanet.owner])

            if not pg.mouse.get_pressed()[0]:
                cls.planetActivelyMoving = False
                if State.startOfGameFreeMovement: #For free movement resets to allow any planet movement
                    State.chosenPlanet = None
                State.readyForBuffer = True
                #TODO - could add processing and visualization of U equipotential lines here

    clickDifference: tuple
    movingLauncher: bool = False
    movingArrow: bool = False
    @classmethod
    def controlLauncher(cls):
        """Called when in Control Launcher Mode"""


        if not cls.movingLauncher and not cls.movingArrow:
            #Check if starting to move launcher
            if pg.mouse.get_pressed()[0]:
                mousepos = pg.Vector2(pg.mouse.get_pos())
                flippedMousePos = pg.Vector2(
                        (mousepos.x - config.windowWidth / 2) * (-1)**(State.activePlayer) + config.windowWidth / 2,
                        (mousepos.y - config.windowHeight / 2) * (-1)**(State.activePlayer) + config.windowHeight / 2
                    )
            
                if State.launcher.iLaunchRect.collidepoint(flippedMousePos):
                    cls.movingLauncher = True
                    cls.clickDifference = (State.launcher.rect.x - flippedMousePos.x, State.launcher.rect.y - flippedMousePos.y)

                
                elif State.launcher.iArrowRect.collidepoint(flippedMousePos):
                    print("Click Arrow")
                    cls.movingArrow = True
                    cls.clickDifference = (State.launcher.iArrowRect.x - mousepos.x, State.launcher.iArrowRect.y - mousepos.y)
                
                elif State.playrects[State.inactivePlayer].collidepoint(flippedMousePos):
                    if State.crosshairs[State.activePlayer] == None:
                        # create crosshair
                        State.crosshairs[State.activePlayer] = pg.sprite.Sprite()
                        State.launchGroups[State.activePlayer].add(State.crosshairs[State.activePlayer])
                        State.crosshairs[State.activePlayer].image = pg.Surface((config.crosshairRadius*2, config.crosshairRadius*2))
                        State.crosshairs[State.activePlayer].rect = State.crosshairs[State.activePlayer].image.get_rect()
                        gfxdraw.circle(State.crosshairs[State.activePlayer].image, config.crosshairRadius, config.crosshairRadius, config.crosshairRadius, (255,255,255))

                    State.crosshairs[State.activePlayer].rect.x = flippedMousePos.x - config.crosshairRadius
                    State.crosshairs[State.activePlayer].rect.y = flippedMousePos.y - config.crosshairRadius
                
        elif cls.movingLauncher: #launcher is moving
            mousepos = pg.Vector2(pg.mouse.get_pos())
            flippedMousePos = pg.Vector2(
                        (mousepos.x - config.windowWidth / 2) * (-1)**(State.activePlayer) + config.windowWidth / 2,
                        (mousepos.y - config.windowHeight / 2) * (-1)**(State.activePlayer) + config.windowHeight / 2
                    )

            State.launcher.rect.x = flippedMousePos.x + cls.clickDifference[0]

            if not pg.mouse.get_pressed()[0]:
                cls.movingLauncher = False
        
        elif cls.movingArrow: #arrow is moving
            mousepos = pg.Vector2(pg.mouse.get_pos())


            State.launcher.iArrowRect.x = mousepos.x + cls.clickDifference[0]
            State.launcher.iArrowRect.x = mousepos.y + cls.clickDifference[1]

            print(State.launcher.iArrowRect)

            if not pg.mouse.get_pressed()[0]:
                cls.movingArrow = False

        State.launcher.rect.clamp_ip(pg.Rect(config.windowWidth/2-config.playFieldWidth/2-State.launcher.rect.width/2, State.launcher.rect.centery, config.playFieldWidth+State.launcher.rect.width, 0))
        

    marker: pg.sprite.Sprite = None
    missile: Missile = None
    leftBoundsTime = 0
    launchedTime = 0
    @classmethod
    def missileLaunched(cls):
        """Called when in Shooting mode"""
        #TODO - make launcher here and add to group if just started
        #TODO - destroy

        print(cls.missile)
        # Define our Missile and group it
        if cls.missile == None:
            print("missile was created!")
            misInitPos = Vector2(State.launcher.rect.center)
            misInitVel = Vector2(0, -config.defaultMissileVel*(-1**State.activePlayer)) #Opposite directio based on player (player on opposite side of board)
            cls.missile = Missile(config.missileRadius, misInitPos, misInitVel)
            State.playerGroups[State.activePlayer].add(cls.missile)
            cls.launchedTime = time.time()

        if time.time() - cls.launchedTime > 20:
            print("switched due to timeout")
            cls.missile.kill()
            cls.missile = None

            # State.movingPlanetsMode = True
            # State.missileLaunchedMode = False
            # State.switchPlayer()
            ui.switchModeFromExplodingMissile()
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

                # State.movingPlanetsMode = True
                # State.missileLaunchedMode = False
                # State.switchPlayer()
                ui.switchModeFromExplodingMissile()
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
                if planet in State.planetGroups[State.inactivePlayer] and State.crosshairs[State.activePlayer].rect.collidepoint(cls.missile.rect.center):
                    planet.kill()
                    print("killed enemy planet! with radius " + str(planet.radius))

                cls.missile.kill()
                cls.missile = None

                # State.movingPlanetsMode = True
                # State.missileLaunchedMode = False
                # State.switchPlayer()
                ui.switchModeFromExplodingMissile()
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