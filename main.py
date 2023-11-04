import pygame
from gameFuncs import GameFuncs
from state import State
import bodies
from pygame import freetype, color

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
running = True

group = pygame.sprite.Group()


#Make planets - Can randomize
planets = pygame.sprite.Group()
p1 = bodies.Planet(30,100,pygame.color.Color("green"))
p2 = bodies.Planet(60,800,pygame.color.Color("blue"))
p3 = bodies.Planet(10,90,pygame.color.Color("purple"))
p4 = bodies.Planet(16,500,pygame.color.Color("magenta"))
planets.add(p1,p2,p3,p4)

#Store planets in state

group.add(p1, p2, p3, p4)

State.setPlanets(planets)

for p in group.sprites():
    p.randomizePosition()
    p.debugDisplay()

while running:
    GameFuncs.movePlanet()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    
    group.update(screen)
    group.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
