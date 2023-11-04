import pygame as pg
from typing import List
from bodies import Planet

class State:
    """Holds all state of game, imported by most files, state edited through functions"""
    
    #Main State
    gameRunning = True

    currentPlayer:int = 0 #Should be 0, 1, or None

    planets: 'pg.sprite.Group[Planet]' = pg.sprite.Group()
    @classmethod
    def addToPlanets(cls, planets):
        #planets can be sprite, or list of sprites, or group
        cls.planets.add(planets)
    
    p0Planets: pg.sprite.Group = pg.sprite.Group()
    @classmethod
    def addToP0Planets(cls, sprites): 
        #sprites can be sprite, or list of sprites, or group
        cls.p0Planets.add(sprites)
    
    p1Planets: pg.sprite.Group = pg.sprite.Group()
    @classmethod
    def addToP1Planets(cls, sprites): 
        #sprites can be sprite, or list of sprites, or group
        cls.p1Planets.add(sprites)

    p0Group: pg.sprite.Group = pg.sprite.Group()
    @classmethod
    def addToP0Group(cls, sprites): 
        #sprites can be sprite, or list of sprites, or group
        cls.p0Group.add(sprites)

    p1Group: pg.sprite.Group = pg.sprite.Group()
    @classmethod
    def addToP1Group(cls, sprites): 
        #sprites can be sprite, or list of sprites, or group
        cls.p1Group.add(sprites)
    
    movingPlanetsMode = False
    choosingProjectileMode = False
    bufferMode = False




    def makePlanet(radius, mass, color, owner: int):
        """Makes a planet and adds to proper group, randomizes position inside player region"""
        #Make planet
        newPlanet = Planet(radius,mass,color, owner)

        #Add to groups
        State.addToPlanets(newPlanet)
        if owner == 0:
            State.addToP0Planets(newPlanet)
            State.addToP0Group(newPlanet)
        elif owner == 1:
            State.addToP1Planets(newPlanet)
            State.addToP1Group(newPlanet)
        
        #Randomize position
        newPlanet.randomizePosition() #TODO - should get position in correct position for given player
        newPlanet.debugDisplay()