import pygame as pg
from typing import List
from bodies import Planet
from launcher import Launcher
import assets

class State:
    """Holds all state of game, imported by most files, state edited through functions"""
    
    #Main State
    gameRunning = True

    activePlayer, inactivePlayer = 0, 1 #Should be 0, 1, or 2. Inactive Player always holds last state, active player sometimes gets set to 2 (buffer mode, no active player)

    #groups!!!
    planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p0Planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p1Planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    launcher: Launcher = None
    p0Group: pg.sprite.Group = pg.sprite.Group()
    p1Group: pg.sprite.Group = pg.sprite.Group()
    passGroup: pg.sprite.Group = pg.sprite.Group()

    #buttons
    UIGroup: pg.sprite.Group = pg.sprite.Group()
    button1 = None #feels weird to store these here, might want to change how this works - initialised in ui
    button2 = None
    announcementBar = None #TODO - what type is this? Label here

    #group for fx layers
    fxGroup: pg.sprite.Group = pg.sprite.Group()

    #group for bg
    bgGroup: pg.sprite.Group = pg.sprite.Group()

    playrects = []

    playerGroups = [p0Group, p1Group, passGroup]
    planetGroups = [p0Planets, p1Planets]
    
    #Different game states
    movingPlanetsMode = False
    chosenPlanet = None
    aimingMissileMode = False
    missileLaunchedMode = False
    readyForBufferMode = False
    bufferMode = False
    
    #Some vars for specific game states
    chosenPlanet:Planet = None #Set when moving, set to none at start of moving phase
    startOfGameFreeMovement = True #Allows free movement of all planets on side (not locked to one planet) for start of game
    

    assetbank = assets

    def switchPlayer():
        #Does switch based on what inactive player was
        State.activePlayer = State.inactivePlayer
        State.inactivePlayer = int(not bool(State.inactivePlayer))