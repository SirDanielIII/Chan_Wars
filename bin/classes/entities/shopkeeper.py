import random
import pygame as pg


class ShopKeep:
    def __init__(self, screen):
        self.deck = None
        self.screen = screen
        self.stock = None
        self.cards = None
        self.image_dict = None
        self.width = 50
        self.height = 50

    def initialize(self, config, deck, images):
        self.image_dict = images
        self.deck = deck
        self.cards = config

    def create_stock(self):
        pos_list = [((a % 3) * 150, (a % 2) * 200) for a in range(6)]
        self.stock = {card[0]: [random.randint(100, 150), pg.Rect(pos_list[num][0], pos_list[num][1], self.width, self.height),
                                self.image_dict[card[0]], card[1]] for num, card in enumerate(random.sample(list(self.cards.items()), 6))}

    def sell(self, mouse_pos):
        for card in self.stock:
            if self.stock[card][1].collidepoint(mouse_pos):
                self.deck.append(card)

    def draw(self):
        for card in self.stock:
            self.screen.blit(self.stock[card][2], (self.stock[card][1].x, self.stock[card][1].y))
