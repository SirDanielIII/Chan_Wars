
import sys
import time

import pygame as pg

from bin.classes.audio import Audio
from bin.levels.main_menu import MainMenu

pg.init()

width = 1600
height = 900

surface = pg.display.set_mode((width, height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA and pg.FULLSCREEN)

running = True


while running:
    for event in pg.event.get():
        pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
        if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
    surface.fill((0, 0, 0))
    pg.display.update()

