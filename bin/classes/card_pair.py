import random
import pygame as pg
from bin.classes.level import Level

pg.font.init()


def redraw_screen(surface, pos_mod, background=None):
    pg.display.update()
    surface.fill((255, 255, 255))
    if background:
        surface.blit(background, (0, pos_mod))


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

    def choose(self, m_pos, choose_boolean):
        if choose_boolean:
            if self.position1[0] < m_pos[0] < self.position1[0] + self.size[0] and self.position1[1] < m_pos[1] < \
                    self.position1[1] + self.size[1]:
                self.chosen1 = 1
            if self.position2[0] < m_pos[0] < self.position2[0] + self.size[0] and self.position2[1] < m_pos[1] < \
                    self.position2[1] + self.size[1]:
                self.chosen2 = 1

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

    def generate_pairs(self, size, m, o_set):
        image_collection = random.sample([a for a in range(self.rows * self.columns)], self.rows * self.columns)
        pos_list = [(a, b, image_collection.pop(-1)) for a in range(self.columns) for b in range(self.rows)]
        self.card_set = [CardPair(self.image_list[card1[2] // 2], ((card1[:2]), (card2[:2])), size, m, self.columns, o_set)
                         for card1 in pos_list for card2 in pos_list if card1[2] + 1 == card2[2] and card2[2] % 2]
        return self.card_set

    def draw_cards(self, m_pos, chosen_cards, background, pos_mod, choose_boolean):
        if chosen_cards < 2:
            for pair in self.card_set:
                pair.choose(m_pos, choose_boolean)
        for pair in self.card_set:
            pair.draw_matching(self.image_list[-1], self.screen, pos_mod)
        redraw_screen(self.screen, pos_mod, background)

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

    def run(self, X, Y, size, margins, matches, delay, background):
        clock = pg.time.Clock()
        offset = [(X - (margins[0] + size[0]) * self.columns) / 2, (Y - (margins[1] + size[1]) * self.rows) / 2]
        word = pg.font.SysFont('Comic Sans MS', 20)
        time = 0
        correct_matches = 0
        f = [0]
        time_start = close_time = pg.time.get_ticks()
        pairs = self.generate_pairs(size, margins, offset)
        s = 1
        while matches or close_time + delay[0] > pg.time.get_ticks():
            pos_mod = move_screen(s, time_start, pg.time.get_ticks(), Y)
            if not pairs:
                pairs = self.generate_pairs(size, margins, offset)
            mouse_pos = [0, 0]
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = list(pg.mouse.get_pos())
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    matches = 0
            self.draw_cards(mouse_pos, f[0], background, pos_mod, matches and not close_time + delay[0] > pg.time.get_ticks())
            f = self.complete()
            if f[0] == 2:
                if not time:
                    time = pg.time.get_ticks()
                if pg.time.get_ticks() > time + delay[1]:
                    correct_matches += f[2]
                    matches -= f[1]
                    self.reset()
                    time = 0
                    if not matches:
                        s = 0
                        close_time = time_start = pg.time.get_ticks()
            text = word.render("Energy: " + str(matches), True, (255, 0, 0))
            self.screen.blit(text, (20, 10 + pos_mod))
            clock.tick(60)
        return correct_matches, True


def move_screen(in_out, time_start, current_time, Y):
    if in_out:
        pos = Y - Y / (1 + 5 ** (-((current_time - time_start) * 1 / 100) + 5))
    else:
        pos = Y / (1 + 5 ** (-((current_time - time_start) * 1 / 100) + 5))
    return pos
