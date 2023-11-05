import pygame as pg
from typing import List
from bodies import Planet
from launcher import Launcher

class State:
    """Holds all state of game, imported by most files, state edited through functions"""
    
    #Main State
    gameRunning = True

    activePlayer, inactivePlayer = 0, 1 #Should be 0, 1, or None

    planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p0Planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    p1Planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    launcher: Launcher = None
    p0Group: pg.sprite.Group = pg.sprite.Group()
    p1Group: pg.sprite.Group = pg.sprite.Group()

    passGroup: pg.sprite.Group = pg.sprite.Group()

    playerGroups = [p0Group, p1Group, passGroup]
    planetGroups = [p0Planets, p1Planets]
    
    movingPlanetsMode = False
    aimingMissileMode = False
    missileLaunchedMode = False

    bufferMode = False

    def switchPlayer():
        State.inactivePlayer = State.activePlayer
        State.activePlayer = int(not bool(State.activePlayer))

    def makePlanet(radius, mass, color, owner: int):
        """Makes a planet and adds to proper group, randomizes position inside player region"""
        #Make planet
        newPlanet = Planet(radius,mass,color, owner)

        #Add to groups
        State.planets.add(newPlanet)
        State.planetGroups[owner].add(newPlanet)
        State.playerGroups[owner].add(newPlanet)
        
        #Randomize position
        newPlanet.randomizePosition() #TODO - should get position in correct position for given player
        newPlanet.debugDisplay()