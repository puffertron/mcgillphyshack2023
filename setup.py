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
    player0Area.rect.y = player1Area.rect.height + config.topOfPlayField
    #bottom
    player1Area.rect.x = config.leftOfPlayField
    player1Area.rect.y = config.topOfPlayField

    State.playrects = [player0Area.rect, player1Area.rect]

    #make ui
    ui.makeButtons()

def setupBackgrounds():
    bg = pg.sprite.Sprite(State.bgGroup)
    bg.image = State.assetbank.BG_ART[0]
    bg.image = pg.transform.smoothscale(bg.image, (config.windowWidth, config.windowHeight))
    bg.rect = pg.Rect(0, 0, config.windowWidth, config.windowHeight)

    #striped border
    bgborder = effects.ScrollSprite()
    bgborder.image = pg.Surface((config.windowWidth, config.windowHeight))
    bgborder.mask = State.assetbank.BG_ART[1]
    bgborder.mask = pg.transform.smoothscale(bgborder.mask,(config.windowWidth, config.windowHeight))
    bgborder.scrolltexture = State.assetbank.BG_ART[2]

    #dust
    bgdust = effects.ScrollSprite()
    bgdust.image = pg.Surface((config.windowWidth, config.windowHeight))
    bgdust.image.set_alpha(50)
    bgdust.mask = State.assetbank.BG_ART[4]
    bgdust.scrolltexture = State.assetbank.BG_ART[3]
    bgdust.scrollspeed = (-1,1)


    #asteroids
    # asteroids1 = effects.ScrollSprite()
    # asteroids1.image = pg.Surface((config.windowWidth, config.windowHeight))
    # asteroids1.scrolltexture = pg.Surface((config.windowWidth, config.windowHeight))
    # asteroids1.scrolltexture.fill((0,0,0))
    # asteroids1.scrolltexture.blit(State.assetbank.ASS[0], asteroids1.scrolltexture.get_rect())
    # asteroids1.scrolltexture = State.assetbank.ASS[0]
    # asteroids1.mask = pg.Surface((config.windowWidth, config.windowHeight))
    # asteroids1.mask.fill((255,255,255))
    # asteroids1.scrollspeed=(1,0)

    asteroids = pg.sprite.Sprite()
    asteroids.image = State.assetbank.ASS[0]
    asteroids.image = pg.transform.smoothscale(asteroids.image, (config.windowWidth, config.windowHeight))
    asteroids.rect = asteroids.image.get_rect()
    asteroids.image.set_colorkey((0,0,0))

    asteroids1 = effects.ScrollSprite()
    asteroids1.image = pg.Surface((config.windowWidth, config.windowHeight))
    asteroids1.scrolltexture = State.assetbank.ASS[1]
    asteroids1.mask = pg.Surface((config.windowWidth, config.windowHeight))
    asteroids1.mask.fill((255,255,255))
    asteroids1.scrollspeed=(1,0)

    State.bgGroup.add(bgborder, bgdust)
    State.fxGroup.add(asteroids, asteroids1)


def setupEffects():
    fx1 = effects.GlobalEffects()
    fx2 = effects.GlobalEffects()
    fxSpecificPlayers = effects.GlobalEffects()
    fxSpecificPlayers.newlayer()
    State.fxGroup.add(fx1)
    State.fxGroup.add(fx2)
    State.fxGroup.add(fxSpecificPlayers)
    State.fx1 = fx1
    State.fx2 = fx2
    State.fxSpecificPlayers = fxSpecificPlayers


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
        newPlanet.randomizePosition(pg.Vector2(config.leftOfPlayField, config.topOfPlayField + (config.topOfPlayField * int(not bool(owner)))),
                                    pg.Vector2(config.leftOfPlayField + config.playFieldWidth, config.topOfPlayField + (config.topOfPlayField * int(not bool(owner))) + config.playFieldHeight))
    
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
        pos = pg.Vector2(i*spacing + 100, 400)
        makePlanet(config.default_planets[i][0],config.default_planets[i][1],
        config.default_planets[i][2], 0, False, pos)

    for i in range(0,5):
        pos = pg.Vector2(i*spacing + 100, 200)
        makePlanet(config.default_planets[i][0],config.default_planets[i][1],
        config.default_planets[i][2], 1, False, pos)
