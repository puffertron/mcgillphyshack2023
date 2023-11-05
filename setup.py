import pygame as pg
import effects, config, ui
from bodies import Planet
from state import State



def setupGameArea():
    #make areas
    player0Area = effects.GameArea(0)
    player1Area = effects.GameArea(1)

    State.bgGroup.add(player0Area, player1Area)
    #top
    player0Area.rect.x = config.leftOfPlayField
    player0Area.rect.y = config.topOfPlayField
    #bottom
    player1Area.rect.x = config.leftOfPlayField
    player1Area.rect.y = player1Area.rect.height + config.topOfPlayField

    State.playrects = [player0Area.rect, player1Area.rect]

    #make ui
    ui.makeButtons()

def setupBackgrounds():
    bg = pg.sprite.Sprite(State.bgGroup)
    bg.image = State.assetbank.BG_ART[0]
    bg.image = pg.transform.smoothscale(bg.image, (config.windowWidth, config.windowHeight))
    bg.rect = pg.Rect(0, 0, config.windowWidth, config.windowHeight)

    bgborder = effects.ScrollSprite()
    bgborder.image = pg.Surface((config.windowWidth, config.windowHeight))
    bgborder.mask = State.assetbank.BG_ART[1]
    bgborder.mask = pg.transform.smoothscale(bgborder.mask,(config.windowWidth, config.windowHeight))
    bgborder.scrolltexture = State.assetbank.BG_ART[2]

    #State.bgGroup.add(bgborder)


def makePlanet(radius, mass, typei, owner: int, randpos=True, pos=None):
    """Makes a planet and adds to proper group, randomizes position inside player region"""
    #Make planet
    newPlanet = Planet(radius,mass,typei, owner)

    #Add to groups
    State.planets.add(newPlanet)
    State.planetGroups[owner].add(newPlanet)
    State.playerGroups[owner].add(newPlanet)
    
    if randpos:
        #Randomize position
        newPlanet.randomizePosition(pg.Vector2(config.leftOfPlayField, config.topOfPlayField + (config.topOfPlayField * owner)),
                                    pg.Vector2(config.playFieldWidth, config.playFieldHeight))
    
    #TODO - should get position in correct position for given player
    if pos:
        newPlanet.rect.x = pos.x
        newPlanet.rect.y = pos.y

    newPlanet.debugDisplay()

# def makePlanetsRandom():
#     makePlanet(30,100, 0)
#     makePlanet(60,800,pg.color.Color("blue"), 0)
#     makePlanet(10,90,pg.color.Color("cyan"), 0)
#     makePlanet(16,500,pg.color.Color("indigo"), 0)

#     makePlanet(30,100,pg.color.Color("orange"), 1)
#     makePlanet(60,800,pg.color.Color("red"), 1)
#     makePlanet(10,90,pg.color.Color("yellow"), 1)
#     makePlanet(16,500,pg.color.Color("magenta"), 1)

def makePlanetsFixed(spacing):

    for i in range(0,5):
        pos = pg.Vector2(i*spacing + 100, 200)
        makePlanet(config.default_planets[i][0],config.default_planets[i][1],
        config.default_planets[i][2], 0, False, pos)

    for i in range(0,5):
        pos = pg.Vector2(i*spacing + 100, 400)
        makePlanet(config.default_planets[i][0],config.default_planets[i][1],
        config.default_planets[i][2], 1, False, pos)
