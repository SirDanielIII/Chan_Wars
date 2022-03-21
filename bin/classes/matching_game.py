import random
from math import floor


class CardPair:
    def __init__(self, image, pos, size, margins):
        self.size = size
        self.position1 = [(pos[0][0] * size[0]) + (pos[0][0] * margins[0]),
                          (pos[0][1] * size[1]) + (pos[0][1] * margins[1])]
        self.position2 = [(pos[1][0] * size[0]) + (pos[1][0] * margins[0]),
                          (pos[1][1] * size[1]) + (pos[1][1] * margins[1])]
        self.image = image
        self.chosen1 = None
        self.chosen2 = None

    def choose(self, mouse_pos):
        if self.position1[0] < mouse_pos[0] < self.position1[0] + self.size[0]:
            if self.position1[1] < mouse_pos[1] < self.position1[1] + self.size[1]:
                self.chosen1 = True
        if self.position2[0] < mouse_pos[0] < self.position2[0] + self.size[0]:
            if self.position2[1] < mouse_pos[1] < self.position2[1] + self.size[1]:
                self.chosen2 = True

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
    def __init__(self, level, image_list, screen):
        self.rows = 4
        self.columns = 2 * level + 1
        self.image_list = image_list
        self.card_set = []
        self.screen = screen

    def generate_pairs(self, size, margins):
        key_list = random.sample([a for a in range(self.rows * self.columns)], self.rows * self.columns)
        key_list = [(key_list[2 * a], key_list[(2 * a) + 1]) for a in range(int(self.rows * self.columns / 2))]
        image_cards = {image: ((key_list[a][0] % self.columns, floor(key_list[a][0] / self.rows)),
                               (key_list[a][1] % self.columns, floor(key_list[a][1] / self.rows)))
                       for a, image in enumerate(self.image_list)}
        self.card_set = [CardPair(card, image_cards[card], size, margins) for card in image_cards]
        return self.card_set

    def complete(self):
        for card in self.card_set:
            pass
