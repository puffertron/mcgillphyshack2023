import pygame
from gameFuncs import GameFuncs
from state import State
from pygame import freetype, color

pygame.init()
screen = pygame.display.set_mode((1200, 900))
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
                    State.currentPlayer = int(not bool(State.currentPlayer))
    
    # Do logic based on current mode
    if State.movingPlanetsMode:
        GameFuncs.movePlanet()
    if State.choosingProjectileMode:
        pass
    if State.bufferMode:
        pass

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    
    if State.currentPlayer == 0:
        State.p0Group.update(screen) #Doing nothing right now?
        State.p0Group.draw(screen)
    elif State.currentPlayer == 1:
        State.p1Group.update(screen) #Doing nothing right now?
        State.p1Group.draw(screen)
    elif None:
        pass #TODO Can show passing game screen
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
