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

#Make planets
# setup.makePlanetsRandom()
setup.makePlanetsFixed(40)

#TEMP
State.movingPlanetsMode = True


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
                launcher = Launcher(State.activePlayer)
                State.launcher = launcher
                State.playerGroups[State.activePlayer].add(launcher)

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


    # RENDER YOUR GAME HERE
    State.bgGroup.update()
    State.bgGroup.draw(screen)

    State.playerGroups[State.activePlayer].update(screen)
    State.playerGroups[State.activePlayer].draw(screen)

    #draw UI
    State.UIGroup.update()
    State.UIGroup.draw(screen)

    #draw fx layers
    State.fxGroup.update()
    State.fxGroup.draw(screen)

    #TODO Can show passing game screen
   
    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(30)  # limits FPS to 60

pg.quit()
