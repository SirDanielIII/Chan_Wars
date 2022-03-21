
import sys
import time

import pygame as pg

from bin.classes.audio import Audio
from bin.levels.main_menu import MainMenu

pg.init()

width = 1280
height = 720

w = 4  # number of cards horizontally
h = 3  # number of cards vertically

bg = pg.transform.smoothscale(pg.image.load('temp_background.jpg'), (1280, 720))
card = pg.transform.smoothscale(pg.image.load('card.png'), (100, 150))


surface = pg.display.set_mode((width, height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)

running = True


while running:
    for event in pg.event.get():
        pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
        if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
    surface.fill((0, 0, 0))
    surface.blit(bg, (0, 0))

    for i in range(1, w+1):
        for j in range(1, h+1):
            surface.blit(card, (250 + 100*i, 0 + 150*j))

    pg.display.update()
