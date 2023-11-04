import pygame
from pygame import Vector2
from dataclasses import dataclass

@dataclass
class State():
    position: Vector2
    velocity: Vector2

s1 = State(Vector2(), Vector2())