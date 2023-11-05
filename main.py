import pygame
from gameFuncs import GameFuncs
from state import State
import bodies
import missile
from launcher import Launcher
from pygame import freetype, color

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
running = True

#Make planets
State.makePlanet(30,100,pygame.color.Color("green"), 0)
State.makePlanet(60,800,pygame.color.Color("blue"), 0)
State.makePlanet(10,90,pygame.color.Color("purple"), 0)
State.makePlanet(16,500,pygame.color.Color("magenta"), 0)

State.makePlanet(30,100,pygame.color.Color("green"), 1)
State.makePlanet(60,800,pygame.color.Color("blue"), 1)
State.makePlanet(10,90,pygame.color.Color("purple"), 1)
State.makePlanet(16,500,pygame.color.Color("magenta"), 1)


#TEMP
State.movingPlanetsMode = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
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
    State.playerGroups[State.activePlayer].update(screen)
    State.playerGroups[State.activePlayer].draw(screen)
   
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()
