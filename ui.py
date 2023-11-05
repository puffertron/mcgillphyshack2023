import pygame as pg
from state import State
import config
from typing import List
from launcher import Launcher
#Controls buttons and boxes with info, also controls changing between modes (since mostly controlled by buttons)
#Note: Would be nice to figure out a better place for things to be handling the state changes, they don't really belong here

def makeButtons():
    b1 = Button(startBegPlayerMovement, pg.Vector2(510, 600), "START GAME!", pg.color.Color(255, 0, 0)) #TODO Make available everywhere
    State.button1 = b1
    State.UIGroup.add(b1)
    b2 = Button(test, pg.Vector2(510, 650), "button 2", pg.color.Color(255, 0, 0))
    State.button2 = b2
    State.UIGroup.add(b2)
    #TODO Make buttons that look pretty

    #Make announcement bar
    #TODO

def startBegPlayerMovement(): #TEMP maybe? Not sure how to do starting stuff
    #Starts first player placement
    State.movingPlanetsMode = True
    State.button1.updateText("go to buffer")
    State.button1.callback = enterStartBufferMode
    State.button2.updateText("button2")
    State.button2.callback = print

def enterStartBufferMode(): #TEMP maybe? Not sure how to do starting stuff
    State.activePlayer = 2 #Sets to no active player so nothing revealed during computer switch
    State.movingPlanetsMode = False
    State.bufferMode = True
    State.button1.updateText("place next planets")
    State.button1.callback = startSecondBegPlayerMovement
    State.button2.updateText("button2")
    State.button2.callback = print
    

def startSecondBegPlayerMovement(): #TEMP maybe? Not sure how to do starting stuff
    State.switchPlayer()
    State.movingPlanetsMode = True
    State.button1.updateText("go to buffer")
    State.button1.callback = enterBufferMode
    State.button2.updateText("button2")
    State.button2.callback = print

def test():
    print("ycfytfcyvjytb!!!!")

#Making the buttons for each mode
def startNewTurn():
    #starts turn showing options for turn, also switches player
    State.switchPlayer()
    State.movingPlanetsMode = False #Just to make sure state is correct, shouldn't change anything, mostly for debugging right now
    State.button1.updateText("move planet")
    State.button1.callback = enterMovePlanetMode
    State.button2.updateText("shoot missile")
    State.button2.callback = enterAimingMissileMode

def enterMovePlanetMode():
    #Goes to moving planet mode from initial mode
    #TODO - deactivate first mode state
    State.chosenPlanet = None
    State.movingPlanetsMode = True
    State.button1.updateText("go to buffer")
    State.button1.callback = enterBufferMode #Iffy to set this button already
    State.button2.updateText("button 2")
    State.button2.callback = print

def enterAimingMissileMode():
    #Goes to aiming from turn choice
    State.aimingMissileMode = True
    State.button1.updateText("launch missile")
    State.button1.callback = enterMissileSimulationMode
    State.button2.updateText("button 2")
    State.button2.callback = print #TODO should make this something useless

    #TEMP - should do in missile.py
    launcher = Launcher(State.activePlayer)
    State.launcher = launcher
    State.playerGroups[State.activePlayer].add(launcher)

def enterMissileSimulationMode():
    #Goes from aiming to simulating missile - when explodes calls next function
    if not State.crosshairs[State.activePlayer] == None:
        State.aimingMissileMode = False
        State.missileLaunchedMode = True

def switchModeFromExplodingMissile():
    State.missileLaunchedMode = False
    #TODO - maybe go to nice new mode to show things nicely?
    State.button1.updateText("go to buffer")
    State.button1.callback = enterBufferMode

def enterBufferMode():
    #Go to buffer mode, should then pass to other player
    State.startOfGameFreeMovement = False #Only needs to be run once first time this is run, this is the only toggle, silly to be here
    State.activePlayer = 2 #Sets to no active player so nothing revealed during computer switch
    State.missileLaunchedMode = False
    State.movingPlanetsMode = False
    State.bufferMode = True
    State.button1.updateText("start turn")
    State.button1.callback = startNewTurn




class Button(pg.sprite.Sprite):
    
    def __init__(self, callback, pos:pg.Vector2, text, color=pg.color.Color(155, 155, 155)):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.surface.Surface((100,20))
        self.color = color
        self.image.fill(self.color)
        self.rect = pg.Rect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.callback = callback
        self.font = pg.freetype.SysFont(pg.freetype.get_default_font(), 12)
        self.text = text
        fontimg, fontrect =self.font.render(self.text)
        self.image.blit(fontimg, fontrect) 
        self.mousedown = [0,0]
    
    def onclick(self):
        print("doing button action: ", self.callback)
        self.callback()
    
    def updateText(self, text):
        self.text = text
        fontimg, fontrect =self.font.render(self.text)
        self.image.fill(self.color)
        self.image.blit(fontimg, fontrect)

    def onhover(self):
        pass

    def update(self):
        self.mousedown[0]=pg.mouse.get_pressed()[0]
        mousep = pg.mouse.get_pos()

        if self.rect.collidepoint(mousep):
            self.onhover()
            if pg.mouse.get_pressed()[0] and self.mousedown[0] != self.mousedown[1]:
                self.onclick()
                self.clicked = True
        self.mousedown[1] = self.mousedown[0]

class TextBox(pg.sprite.Sprite):
    
    def __init__(self, pos:pg.Vector2, text, textColor=pg.color.Color(255, 255, 255), backColor=pg.color.Color(255, 0, 0)):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.surface.Surface((60,20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.callback = callback
        self.font = pg.freetype.SysFont(pg.freetype.get_default_font(), 12)
        self.text = text
        self.font.render_to(self.image, self.rect, self.text) #TODO - fix position of text
        self.mousedown = [0,0]