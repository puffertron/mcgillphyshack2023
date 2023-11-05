import pygame as pg
from typing import List
from bodies import Planet

class State:
    """Holds all state of game, imported by most files, state edited through functions"""
    
    #Main State
    gameRunning = True

    activePlayer, inactivePlayer = 0, 1 #Should be 0, 1, or None

    #groups!!!
    planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p0Planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p1Planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p0Group: pg.sprite.Group = pg.sprite.Group()
    p1Group: pg.sprite.Group = pg.sprite.Group()
    passGroup: pg.sprite.Group = pg.sprite.Group()

    #group for fx layers
    fxGroup: pg.sprite.Group = pg.sprite.Group()

    #group for bg
    bgGroup: pg.sprite.Group() = pg.sprite.Group()

    playrects = []

    playerGroups = [p0Group, p1Group, passGroup]
    planetGroups = [p0Planets, p1Planets]
    
    movingPlanetsMode = False
    aimingMissileMode = False
    missileLaunchedMode = False

    bufferMode = False

    def switchPlayer():
        State.inactivePlayer = State.activePlayer
        State.activePlayer = int(not bool(State.activePlayer))