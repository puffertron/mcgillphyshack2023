import pygame
from pygame import Vector2
from dataclasses import dataclass, field
import config

@dataclass
class Kinematics:
    pos: Vector2 = Vector2
    vel: Vector2 = Vector2
    acc: Vector2 = Vector2

    posHist: [Vector2] = field(default_factory = lambda: [])
    velHist: [Vector2] = field(default_factory = lambda: [])
    accHist: [Vector2] = field(default_factory = lambda: [])

    maxHistLen: int = -1

    def nextPosYI4(self, planets):
        self.saveValsToHist()
        pass

    # Leapfrog Method
    def nextPosLF(self, planets):
        pass


    # Semi-implicit Euler Method
    def nextPosSIE(self, planets):
        self.acc = self.acceleration(planets)
        self.saveValsToHist()
        self.vel += self.acc
        self.pos += self.vel



    def acceleration(self, planets):
        a = Vector2()
        for p in planets:
            xp = xp = Vector2(p.rect.center) # position of planet

            # the contribution of each planet to the acceleration is
            # Mp * [ (x_diff) x^ + (y_diff) y^ ] / ||r_diff||^3
            a += p.mass*(self.pos - xp)/(((self.pos - xp).length())**3)

        # Multiply by our gravity  
        a *= config.gravity
        return a
        

    def saveValsToHist(self):
        self.posHist.append(self.pos)
        self.velHist.append(self.vel)
        self.accHist.append(self.acc)

        if self.maxHistLen >= 0 and len(self.posHist) > self.maxHistLen:
            self.posHist.pop(0)
            self.posHist.pop(0)
            self.posHist.pop(0)

    def showHist(self):
        out = []
        for i in range(len(self.posHist)):
            out[i] = [self.postHist[i], self.velHist[i], self.accHist[i]]
        print(out)