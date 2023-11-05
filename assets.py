import pygame as pg

PLANETS_ART = [
    pg.image.load("assets/planets/hack23-planet-dwarf.png"),
    pg.image.load("assets/planets/hack23-planet-gasgiant.png"),
    pg.image.load("assets/planets/hack23-planet-mini-neptune.png"),
    pg.image.load("assets/planets/hack23-planet-neutronstar.png"),
    pg.image.load("assets/planets/hack23-planet-terrestrial.png"),
]

BG_ART = [
    pg.image.load("assets/bg/hack23-bg-base.png"),
    pg.image.load("assets/bg/hack23-bg-border-mask.png"),
    pg.image.load("assets/bg/hack23-bg-border-texture.png"),
    pg.image.load("assets/bg/hack23-bg-dust-texture.png"),
    pg.image.load("assets/bg/hack23-dust-texture-mask.png"),  
]

UI_ELEMENTS = [
    pg.image.load("assets/ui/hack23-textbox-active.png"),
    pg.image.load("assets/ui/hack23-textbox-idle.png"),
    pg.image.load("assets/ui/hack23-playarea-border.png")
]

ASS = [
    pg.image.load("assets/asteroid/hack23-asteriodbelt-back.png"),
    pg.image.load("assets/asteroid/hack23-asteriodbelt-front.png")
]