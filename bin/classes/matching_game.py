import pygame as pg
import random
from math import floor


class CardPair:
    def __init__(self, image, pos):
        self.position1 = pos[0]
        self.position2 = pos[1]
        self.image = image


class Screen:
    def __init__(self, level, image_list):
        self.rows = 4
        self.columns = 2 * level
        self.image_list = image_list

    def generate_pairs(self, size, margins):
        key_list = [a for a in range(self.rows * self.columns)]
        key_list = random.sample(key_list, len(key_list))
        image_cards = [(self.image_list[floor(a/2)-1], (a % self.columns, floor(a / self.rows))) for a in key_list]
        screen_complete = [CardPair(pair[0], pair[1]) for pair in image_cards]

