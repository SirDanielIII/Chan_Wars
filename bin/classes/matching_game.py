import random
import pygame
from math import floor


class CardPair:
    def __init__(self, image, pos, size, margins):
        self.size = size
        self.position1 = [pos[0][0] * (size[0] + margins[0]) + 50, pos[0][1] * (size[1] + margins[1]) + 50]
        self.position2 = [pos[1][0] * (size[0] + margins[0]) + 50, (pos[1][1] * (size[1] + margins[1])) + 50]
        self.image = image
        self.chosen1 = 0
        self.chosen2 = 0

    def choose(self, m_pos):
        if self.position1[0] < m_pos[0] < self.position1[0] + self.size[0]:
            if self.position1[1] < m_pos[1] < self.position1[1] + self.size[1]:
                self.chosen1 = 1
        if self.position2[0] < m_pos[0] < self.position2[0] + self.size[0]:
            if self.position2[1] < m_pos[1] < self.position2[1] + self.size[1]:
                self.chosen2 = 1

    def draw_matching(self, default, screen):
        if self.chosen1:
            screen.blit(self.image, self.position1)

        else:
            screen.blit(default, self.position1)
        if self.chosen2:
            screen.blit(self.image, self.position2)
        else:
            screen.blit(default, self.position2)


class MatchingScreen:
    def __init__(self, lvl, images, screen):
        self.rows = 4
        self.columns = 2 * lvl + 1
        self.image_list = images
        self.card_set = []
        self.screen = screen

    def generate_pairs(self, size, margins):
        key_list = random.sample([a+1 for a in range(self.rows * self.columns)], self.rows * self.columns)
        key_list = [(key_list[2 * a], key_list[(2 * a) + 1]) for a in range(int(self.rows * self.columns / 2))]
        image_cards = {image: ((floor((key_list[a][0]-1) / self.columns), (key_list[a][0]-1) % self.columns),
                               (floor((key_list[a][1]-1) / self.columns), (key_list[a][1]-1) % self.columns))
                       for a, image in enumerate(self.image_list)}
        self.card_set = [CardPair(card, image_cards[card], size, margins) for card in image_cards]
        return self.card_set

    def draw_cards(self, default):
        for pair in self.card_set:
            pair.draw_matching(default, self.screen)
        redraw_screen(self.screen)

    def complete(self):
        count = 0
        for a in self.card_set:
            if a.chosen1 + a.chosen2 == 2:
                return 2
            else:
                count += a.chosen1 + a.chosen2
        return count

    def reset(self):
        for m, a in enumerate(self.card_set):
            if a.chosen1 + a.chosen2 == 2:
                self.card_set.pop(m)
            a.chosen1 = 0
            a.chosen2 = 0


def redraw_screen(surface):
    pygame.display.update()
    surface.fill((255, 255, 255))

