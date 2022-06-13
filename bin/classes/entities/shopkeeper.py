import random
import pygame as pg


class ShopKeep:
    def __init__(self, config, images, screen):
        self.deck = None
        self.screen = screen
        self.stock = None
        self.cards = config["player"]["cards"]
        self.image_dict = images

    def initialize(self, deck):
        self.deck = deck
        self.stock = {card: [random.randint(100, 150), pg.Rect(100 * num, 100 * num, 50, 50), self.image_dict[card]] for num, card in enumerate(random.sample(self.cards, 6))}

    def sell(self, mouse_pos):
        for card in self.stock:
            if self.stock[card][1].collidepoint(mouse_pos):
                self.deck.append(card)

    def draw(self):
        for card in self.stock:
            self.screen.blit(self.stock[card][2], (self.stock[card][1].x, self.stock[card][1].y))
