import pygame

#This file just holds config constants that we might want to change, things like screen resolution

windowWidth = 600
windowHeight = 700

playFieldWidth = 400
playFieldHeight = 300

topOfPlayField = 50
leftOfPlayField = 100

gravity = -1

missileRadius = 5
markerSize = 6

# Launcher Position things
launchLine = 20 # from edge of screen
launcherRadius = 10 # drawn launcher object radius
arrowAreaRadius = 100 # area from launcher that the arrow is allowed to go
arrowheadRadius = 5

defaultMissileVel = 5 #Might not be used

crosshairRadius = 15

crosshairRadius = 15

# Default Planet Attributes - tuples of (radius, mass, type)
default_planets = [
    (10, 800, 3),  # neutron star - tiny radius, large mass     - NEUTRON STAR      - white
    (50, 90, 1), # gas giant - large radius, tiny mass        - gassy, large      - pinkish
    (20, 150, 4), # terrestrial - medium radius, medium mass   - cratery, medium   - greeny
    (30, 120, 2), # mini-neptune - medium radius, medium mass  - gassy, medium     - blue/purple
    (15, 40, 0)   # dwarf - small radius, small mass           - cratery, small    - purpley grey
]


p0colors = ["green", "blue", "cyan", "indigo", "darkgreen"]
p1colors = ["red", "orange", "magenta", "yellow", "purple"]

#types:
# cratery
# gassy
# big, medium, small