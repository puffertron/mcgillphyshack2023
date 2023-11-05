import pygame as pg
from state import State


def makePotentialMatrix():
    #Uses current planet configuration to calc potential
    #TODO - make differential version for better computing speed
    State.potentialMatrix(np.zeros(shape=(config.playFieldWidth,config.playFieldHeight)))
    for planet in State.planetGroups:
        matrixToAdd = np.zeros(shape=(config.playFieldWidth,config.playFieldHeight))
        planet.rect.center
        planet.radius

        #Get coords of planet for matrix coords
        planetx = planet.rect.center[0]
        planety = planet.rect.center[1]

        # for pixxpos in range(TODO):
        #     for pixypos in range
        