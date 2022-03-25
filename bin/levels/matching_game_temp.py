
import sys
import time
import os
import pygame as pg

from bin.classes.audio import Audio
from bin.tools.colours import *
from bin.levels.main_menu import MainMenu

pg.init()

width = 1280
height = 720
count = 0

w = 3  # number of cards horizontally
h = 4  # number of cards vertically

card_x = 100
card_y = 150
offset_x = card_x + 290
offset_y = card_y-65

bg = pg.transform.smoothscale(pg.image.load('bg.jpg'), (1280, 720))
card = pg.transform.smoothscale(pg.image.load('Mr_Chan.png'), (card_x, card_y))

word = pg.font.SysFont('In your face, Joffrey!', 50)

energy = 2

surface = pg.display.set_mode((width, height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)

running = True


def generate_cards(card, energy):
    text = word.render("Energy: "+str(energy), True, white)  # number of lines
    surface.blit(text, (20, 10))

    for i in range(1, w+1):
        for j in range(1, h+1):
            surface.blit(card, (offset_x-(50*(w-3)) + card_x*i, -offset_y + card_y*j))


while running:
    for event in pg.event.get():
        pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
        if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            count += 1
    surface.fill((0, 0, 0))
    surface.blit(bg, (0, 0))

    if count == 2:
        energy -= 1
        count = 0

    generate_cards(card, energy)

    pg.display.update()
