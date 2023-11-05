import pygame
from gameFuncs import GameFuncs
from state import State
import bodies
import missile
from pygame import freetype, color
import config

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
running = True


#Make planets
for i, (radius, mass) in enumerate(config.default_planets):
    State.makePlanet(radius, mass, pygame.color.Color(config.temp_colors[i]), 0)

for i, (radius, mass) in enumerate(config.default_planets):
    State.makePlanet(radius, mass, pygame.color.Color(config.temp_colors[i]), 1)

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
    State.playerGroups[State.activePlayer].update(screen)
    State.playerGroups[State.activePlayer].draw(screen)
   
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()
