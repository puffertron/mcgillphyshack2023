import pygame as pg
from gameFuncs import GameFuncs
from state import State
import bodies, missile, effects
from pygame import freetype, color

pg.init()
screen = pg.display.set_mode((600, 800))
clock = pg.time.Clock()
running = True

player0Area = effects.GameArea(0)
player1Area = effects.GameArea(1)

bgGroup = pg.sprite.Group()
bgGroup.add(player0Area, player1Area)

#Make planets
State.makePlanet(30,100,pg.color.Color("green"), 0)
State.makePlanet(60,800,pg.color.Color("blue"), 0)
State.makePlanet(10,90,pg.color.Color("purple"), 0)
State.makePlanet(16,500,pg.color.Color("magenta"), 0)

State.makePlanet(30,100,pg.color.Color("green"), 1)
State.makePlanet(60,800,pg.color.Color("blue"), 1)
State.makePlanet(10,90,pg.color.Color("purple"), 1)
State.makePlanet(16,500,pg.color.Color("magenta"), 1)


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
                    
    
    # Do logic based on current mode
    if State.movingPlanetsMode:
        GameFuncs.movePlanet()
    if State.missileLaunchedMode:
        GameFuncs.missileLaunched()
    if State.bufferMode:
        pass

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")


    # RENDER YOUR GAME HERE
    bgGroup.draw(screen)

    State.playerGroups[State.activePlayer].update(screen)
    State.playerGroups[State.activePlayer].draw(screen)
    #TODO Can show passing game screen
   
    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(30)  # limits FPS to 60

pg.quit()
