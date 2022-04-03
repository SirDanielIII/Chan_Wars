import random
import pygame as pg
from bin.classes.level import Level

pg.font.init()


def redraw_screen(surface, game_canvas, pos_mod, background=None):
    pg.display.update()
    surface.blit(game_canvas, (0, 0))
    if background:
        surface.blit(background, (0, pos_mod))


def move_screen(in_out, time_start, current_time, Y):
    if in_out:
        pos = Y - Y / (1 + 5 ** (((time_start - current_time) / 100) + 7))
    else:
        pos = Y / (1 + 5 ** (((time_start - current_time) / 100) + 7))
    return pos


class CardPair():
    def __init__(self, image, pos, size, m, columns, o_set):
        self.size = size
        self.position1 = [o_set[0] - columns + (size[0] + m[0]) * pos[0][0],
                          o_set[1] + (size[1] + m[1]) * pos[0][1]]
        self.position2 = [o_set[0] - columns + (size[0] + m[0]) * pos[1][0],
                          o_set[1] + (size[1] + m[1]) * pos[1][1]]
        self.image = image
        self.chosen1 = 0
        self.chosen2 = 0

    def choose(self, m_pos, choose_boolean, rect_pair):
        if choose_boolean:
            if rect_pair[0].collidepoint(m_pos):
                self.chosen1 = 1
            if rect_pair[1].collidepoint(m_pos):
                self.chosen2 = 1
            print(self.chosen1, self.chosen2)

    def draw_matching(self, default, screen, pos_mod):
        if self.chosen1:
            screen.blit(self.image, (self.position1[0], self.position1[1] + pos_mod))
        else:
            screen.blit(default, (self.position1[0], self.position1[1] + pos_mod))
        if self.chosen2:
            screen.blit(self.image, (self.position2[0], self.position2[1] + pos_mod))
        else:
            screen.blit(default, (self.position2[0], self.position2[1] + pos_mod))


class MatchingScreen:
    def __init__(self, columns, images, screen):
        self.screen = screen
        self.rows = 4
        self.columns = columns
        self.image_list = images
        self.card_set = []
        self.rect_set = []

    def generate_pairs(self, size, m, o_set):
        image_collection = random.sample([a for a in range(self.rows * self.columns)], self.rows * self.columns)
        pos_list = [(a, b, image_collection.pop(-1)) for a in range(self.columns) for b in range(self.rows)]
        self.card_set = [CardPair(self.image_list[card1[2] // 2], ((card1[:2]), (card2[:2])), size, m, self.columns, o_set)
                         for card1 in pos_list for card2 in pos_list if card1[2] + 1 == card2[2] and card2[2] % 2]
        self.rect_set = [(pg.Rect(card_pair.position1[0], card_pair.position1[1], card_pair.size[0], card_pair.size[1]),
                         pg.Rect(card_pair.position2[0], card_pair.position2[1], card_pair.size[0], card_pair.size[1])) for card_pair in self.card_set]
        return self.card_set

    def draw_cards(self, m_pos, chosen_cards, background, pos_mod, choose_boolean, game_canvas):
        redraw_screen(self.screen, game_canvas, pos_mod, background)
        if chosen_cards < 2:
            for pair in self.card_set:
                pair.choose(m_pos, choose_boolean, self.rect_set[self.card_set.index(pair)])
        for pair in self.card_set:
            pair.draw_matching(self.image_list[-1], self.screen, pos_mod)

    def complete(self):
        count = 0
        for a in self.card_set:
            if a.chosen1 + a.chosen2 == 2:
                return 2, 1, 1
            else:
                count += a.chosen1 + a.chosen2
        return count, 1, 0

    def reset(self):
        for m, a in enumerate(self.card_set):
            if a.chosen1 + a.chosen2 == 2:
                self.card_set.pop(m)
            a.chosen1 = 0
            a.chosen2 = 0
