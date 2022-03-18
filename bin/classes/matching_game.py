import pygame as pg
import random
from math import floor


class CardPair:
    def __init__(self, pos1, pos2, image):
        self.position1 = pos1
        self.position2 = pos2
        self.image = image


class Screen:
    def __init__(self, level, image_list):
        self.rows = 4
        self.columns = 2 * level
        self.image_list = image_list

    def generate_pairs(self, size, margins):
        pos_list = [[[a, b] for b in range(self.rows)] for a in range(self.columns)]
        key_list = [a for a in range(self.rows * self.columns)]
        for m in range(self.rows * self.columns):
            keys = key_list.pop(random.randint(0, len(key_list))), key_list.pop(random.randint(0, len(key_list)))
            pos1 = pos_list[floor(keys[0] // len(pos_list))], pos_list[floor(keys[0] // len(pos_list))][keys[0] % len(pos_list) - 1]
            pos2 =
            image = self.image_list.pop(random.randint(0, len(self.image_list)))

