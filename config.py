import pygame

#This file just holds config constants that we might want to change, things like screen resolution

windowWidth = 600
windowHeight = 700

playFieldWidth = 300
playFieldHeight = 400

topOfPlayField = 50
leftOfPlayField = 100

gravity = -1

missileRadius = 5
markerSize = 6

yposLauncher = 10

# Default Planet Attributes - tuples of (radius, mass)
default_planets = [
    (5, 800),  # neutron star - tiny radius, large mass     - NEUTRON STAR      - white
    (100, 90), # gas giant - large radius, tiny mass        - gassy, large      - pinkish
    (30, 150), # terrestrial - medium radius, medium mass   - cratery, medium   - greeny
    (40, 120), # mini-neptune - medium radius, medium mass  - gassy, medium     - blue/purple
    (15, 40)   # dwarf - small radius, small mass           - cratery, small    - purpley grey
]

p0colors = ["green", "blue", "cyan", "indigo", "darkgreen"]
p1colors = ["red", "orange", "magenta", "yellow", "purple"]

#types:
# cratery
# gassy
# big, medium, small