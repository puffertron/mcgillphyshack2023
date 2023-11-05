import pygame as pg
from gameFuncs import GameFuncs
from state import State
import bodies, missile, effects, setup, config
from launcher import Launcher
from pygame import freetype, color
import config

pg.init()
screen = pg.display.set_mode((config.windowWidth, config.windowHeight))
clock = pg.time.Clock()
running = True

#setup scene
setup.setupBackgrounds()
setup.setupGameArea()
State.p0LaunchGroup.add(State.p0Launcher)
State.p1LaunchGroup.add(State.p1Launcher)

#Make planets
# setup.makePlanetsRandom()
setup.makePlanetsFixed(40)


while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.unicode == "a":
                State.switchPlayer()
            elif event.unicode == "s":
                State.movingPlanetsMode = False
                State.missileLaunchedMode = True
            elif event.unicode == "d":
                State.movingPlanetsMode = True
                State.missileLaunchedMode = False
            elif event.unicode == "f":
                State.aimingMissileMode = True
            #TODO - add detection of button clicks for changing modes
            
                    
    
    # Do logic based on current mode
    if State.movingPlanetsMode:
        GameFuncs.movePlanet()
    if State.aimingMissileMode:
        GameFuncs.controlLauncher()
    if State.missileLaunchedMode:
        GameFuncs.missileLaunched()
    if State.bufferMode:
        pass

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # create drawing surface
    canvas = pg.Surface(screen.get_size())

    # RENDER YOUR GAME HERE
    State.bgGroup.update()
    State.bgGroup.draw(canvas)

    State.playerGroups[State.activePlayer].update(canvas)
    State.playerGroups[State.activePlayer].draw(canvas)

    #draw launch stuff
    if State.aimingMissileMode == True or State.missileLaunchedMode == True:
        State.launchGroups[State.activePlayer].update()
        State.launchGroups[State.activePlayer].draw(canvas)

    #draw fx layers
    State.fxGroup.update()
    State.fxGroup.draw(canvas)

    if State.activePlayer == 1:
        canvas = pg.transform.rotate(canvas, 180)

    screen.blit(canvas, screen.get_rect())

    #draw UI
    State.UIGroup.update()
    State.UIGroup.draw(screen)

    #TODO Can show passing game screen
   
    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(30)  # limits FPS to 60

pg.quit()
