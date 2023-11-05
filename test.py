import pygame as pg
from state import State
import numpy as np
import config

planets:str = None

print(planets)


def makePotentialMatrix():
    #Uses current planet configuration to calc potential
    #TODO - make differential version for better computing speed
    State.potentialMatrix(np.zeros(shape=(config.playFieldWidth,config.playFieldHeight)))
    for planet in State.planets:
        matrixToAdd = np.zeros(shape=(config.playFieldWidth,config.playFieldHeight))
        x_p, y_p = planet.rect.center5
        m_p = planet.mass

        #Get coords of planet for matrix coords
        planetx, planety = planet.rect.center

        #go over planets
        # for pixxpos in range(TODO):
        #     for pixypos in range

def differentialMatrix():
    #Uses current matrix, old planet position, new planet position to recalculate matrix
    pass
    #Not priority