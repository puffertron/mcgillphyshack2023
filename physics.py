import pygame
from pygame import Vector2
import bodies


# Constants
g = 0
dt = 1

p1 = bodies.Planet(30,100,pygame.color.Color("green"))
p2 = bodies.Planet(60,800,pygame.color.Color("blue"))
p3 = bodies.Planet(10,90,pygame.color.Color("purple"))
p4 = bodies.Planet(16,500,pygame.color.Color("magenta"))

planets = [p1, p2, p3, p4]


def acceleration(planets, x):
    a = Vector2()
    for p in planets:
        xp = Vector2(p.rect.center())
        a += p.mass
