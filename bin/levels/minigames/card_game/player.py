import random
from math import floor
from bin.colours import *

import pygame as pg

pg.font.init()


def move_pos(in_out, elapsed_time, y, speed):
    """
    The move screen method was edited to work with elapsed time as opposed to calculating elapsed time using the given values
    Time needs to be based off of milliseconds (framerate independent)
    """
    if in_out:
        pos = y - y / (1 + speed ** (-(elapsed_time * 10) + 7))
    else:
        pos = y / (1 + speed ** (-(elapsed_time * 10) + 7))
    return pos


class Card(object):
    def __init__(self, image, pos, size, m, columns, o_set, card_type):
        self.size = size
        self.position = [o_set[0] + (size[0] + m[0]) * pos[0], o_set[1] + (size[1] + m[1]) * pos[1]]
        self.image = image
        self.chosen = 0
        self.clairvoyant = False
        self.card_type = card_type
        self.collision = pg.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def choose(self, m_pos, choose_boolean):
        if choose_boolean:
            if self.collision.collidepoint(m_pos):
                self.chosen = 1

    def draw(self, default, screen, pos_mod):
        if self.chosen:
            screen.blit(self.image, (self.position[0], self.position[1] + pos_mod))
        else:
            screen.blit(default, (self.position[0], self.position[1] + pos_mod))


class Player:
    def __init__(self, screen, config):
        self.screen = screen
        self.metadata = config
        self.rows = 0
        self.cards = None
        self.columns = 0
        self.image_dict = {}
        self.damage = 0
        self.block = 0
        self.health = 0
        self.energy = 0
        self.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}}
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Energized": 0, "Armor": 0, "Clairvoyant": 0}
        self.acted = False
        self.size = None
        self.choices = {}
        self.ui_rect = None
        self.deck = None
        self.played_cards = None

    def initialize(self, image_dict):
        self.rows = self.metadata["rows"]
        self.cards = self.metadata["cards"]
        self.columns = self.metadata["columns"]
        self.image_dict = image_dict
        self.health = self.metadata["hp"]
        self.deck = self.metadata["base_deck"]
        self.energy = self.metadata["energy"]

    def generate_pairs(self, size, margins, X, Y, deck=None):
        # ------------------------------------------------------------------------------------------------------------------
        if not self.deck:
            self.deck = deck
        self.size = size
        images = {chan.split()[-1]: self.image_dict[chan.split()[-1]] for chan in self.deck}
        o_set = ((X - margins[0] * (self.columns - 1) - self.size[0] * self.columns) / 2 + 2 * self.size[0], (Y - margins[1] * (self.rows - 1) - self.size[1] * self.rows) / 2)
        self.ui_rect = pg.Rect(o_set[0] - 4 * self.size[0], o_set[1], self.size[0] * 3.5, margins[1] * (self.rows - 1) + self.size[1] * self.rows)
        cards = random.sample(self.deck, int((self.columns * self.rows) / 2))
        pos_list = [(a, b) for a in range(self.columns) for b in range(self.rows)]
        random.shuffle(pos_list)
        self.played_cards = [Card(images[cards[floor(a/2)].split()[-1]], position, self.size, margins, self.columns, o_set, cards[floor(a/2)]) for a, position in enumerate(pos_list)]
        return self.played_cards

    def draw_card_screen(self, ui_images, m_pos, chosen_cards, background, pos_mod, choose_boolean):
        self.screen.blit(background, (0, pos_mod))
        if chosen_cards < 2:
            for card in self.played_cards:
                card.choose(m_pos, choose_boolean)
        for card in self.played_cards:
            card.draw(self.image_dict["card_back"], self.screen, pos_mod)
        self.draw_ui(ui_images, pos_mod)

    def draw_ui(self, ui_images, pos_mod):
        pg.draw.rect(self.screen, (224, 255, 255), self.ui_rect, 0, 25)
        pg.draw.rect(self.screen, cyan, self.ui_rect, 5, 25)
        for a in range(self.metadata["energy"]):
            if a < self.energy:
                self.screen.blit(ui_images["energy_full"], (self.ui_rect.x + 5 + a * 75, self.ui_rect.y + 10 + pos_mod))
            else:
                self.screen.blit(ui_images["energy_empty"], (self.ui_rect.x + 5 + a * 75, self.ui_rect.y + 10 + pos_mod))

    def complete(self):
        count = 0
        self.choices = {}
        for a in self.played_cards:
            self.choices[a.card_type] = self.choices.get(a.card_type, 0)
            self.choices[a.card_type] += a.chosen
        for card_type, number in self.choices.items():
            if number == 2 and not self.acted:
                card = card_type.split(" ")
                mod = 1
                if self.status_bar["Weakness"]:
                    mod *= 0.75
                if self.buff_bar["Power"]:
                    mod *= 1.25
                self.attack["damage"] += self.cards[card[-1]]["damage"] * mod
                self.attack["block"] += self.cards[card[-1]]["block"]
                self.attack["heal"] += self.cards[card[-1]]["heal"]
                if self.cards[card[-1]]["status"] != "None":
                    for status in self.cards[card[-1]]["status"]:
                        self.attack["status"][status] = self.attack["status"].get(status, 0)
                        self.attack["status"][status] += self.cards[card[-1]]["status"][status]
                if self.cards[card[-1]]["buff"] != "None":
                    for buff in self.cards[card[-1]]["buff"]:
                        self.attack["buff"][buff] = self.attack["buff"].get(buff, 0)
                        self.attack["buff"][buff] += self.cards[card[-1]]["buff"][buff]
                if len(card) > 1:
                    for upgrade in card[:-1]:
                        self.attack["damage"] += self.cards[card[-1]]["upgrades"][upgrade]["damage"]
                        self.attack["block"] += self.cards[card[-1]]["upgrades"][upgrade]["block"]
                        self.attack["heal"] += self.cards[card[-1]]["upgrades"][upgrade]["heal"]
                        if self.cards[card[-1]]["upgrades"][upgrade]["status"] != "None":
                            for status in self.cards[card[-1]]["upgrades"][upgrade]["status"]:
                                if status == "None":
                                    self.attack["status"] = {status: self.cards[card[-1]]["upgrades"][upgrade]["status"][status]}
                                else:
                                    self.attack["status"][status] = self.attack["status"].get(status, 0)
                                    self.attack["status"][status] += self.cards[card[-1]]["upgrades"][upgrade]["status"][status]
                        if self.cards[card[-1]]["upgrades"][upgrade]["buff"] != "None":
                            for buff in self.cards[card[-1]]["upgrades"][upgrade]["buff"]:
                                if self.attack["buff"] == "None":
                                    self.attack["buff"] = {buff: self.cards[card[-1]]["upgrades"][upgrade]["buff"][buff]}
                                else:
                                    self.attack["buff"][buff] = self.attack["buff"].get(buff, 0)
                                    self.attack["buff"][buff] += self.cards[card[-1]]["upgrades"][upgrade]["buff"][buff]
                if self.buff_bar["Lifesteal"]:
                    self.attack["heal"] += self.attack["damage"]
                if self.buff_bar["Armor"]:
                    self.attack["block"] += self.buff_bar["Armor"]
                self.health += self.attack["heal"]
                if self.health > self.metadata["hp"]:
                    self.health = self.metadata["hp"]
                self.block = self.attack["block"]
                self.acted = True
                return 2, self.attack["damage"], self.attack["status"]
            else:
                count += number
        if count == 2:
            self.acted = True
        return count, 0, "None"

    def reset(self):
        remove_list = []
        for m, a in enumerate(self.played_cards):
            if a.chosen and self.choices[a.card_type] == 2:
                remove_list.append(m)
            a.chosen = 0
        for index in remove_list[::-1]:
            self.played_cards.pop(index)
        self.acted = False

    def update(self, damage, status_effects):
        self.energy = self.metadata["energy"]
        self.energy += self.buff_bar["Energized"]
        if self.status_bar["Vulnerable"]:
            damage *= 1.25
        if self.status_bar["Marked"] and damage:
            damage += self.status_bar["Marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.status_bar["Poison"]
        self.health += self.buff_bar["Regeneration"]
        if self.health > self.metadata["hp"]:
            self.health = self.metadata["hp"]
        self.health -= damage
        for a in self.status_bar:
            if self.status_bar[a]:
                self.status_bar[a] -= 1
        for b in self.buff_bar:
            if self.buff_bar[b]:
                self.buff_bar[b] -= 1
        if status_effects != "None":
            for effect in status_effects:
                self.status_bar[effect] += status_effects[effect]
        if self.attack["buff"] != "None":
            for buff in self.attack["buff"]:
                self.buff_bar[buff] += self.attack["buff"][buff]
