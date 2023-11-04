import pygame as pg
from typing import List
from bodies import Planet

class State:
    """Holds all state of game, imported by most files, state edited through functions"""
    
    #Main State
    gameRunning = True

    planets: 'pg.sprite.Group[Planet]' = None
    missleGroup = pg.sprite.Group()

    @classmethod
    def setPlanets(cls, planets):
        cls.planets = planets