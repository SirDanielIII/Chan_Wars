import random
from math import floor
from bin.colours import *
from bin.blit_tools import *

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
    def __init__(self, image, pos, size, m, o_set, card_type):
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
        self.margins = (20, 30)
        self.block = 0
        self.health = 0
        self.energy = 0
        self.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}}
        self.status_bar = {"Fear": 0, "Weakness": 0, "Vulnerable": 0, "Disappointment": 0, "Pained": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Energized": 0, "Armor": 0, "Clairvoyant": 0}
        self.acted = False
        self.size = None
        self.choices = {}
        self.ui = {}
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
        o_set = ((X - (self.columns - 4.5) * self.size[0] - (self.columns - 1) * margins[0]) / 2, (Y - margins[1] * (self.rows - 1) - self.size[1] * self.rows) / 2)
        self.ui["rect"] = pg.Rect((X - (self.columns + 4.5) * self.size[0] - (self.columns - 1) * margins[0]) / 2, o_set[1], self.size[0] * 4, margins[1] * (self.rows - 1) + self.size[1] * self.rows)
        self.ui["surface"] = pg.Surface((self.size[0] * 4, margins[1] * (self.rows - 1) + self.size[1] * self.rows), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        cards = random.sample(self.deck, int((self.columns * self.rows) / 2))
        pos_list = [(a, b) for a in range(self.columns) for b in range(self.rows)]
        random.shuffle(pos_list)
        self.played_cards = [Card(images[cards[floor(a/2)].split()[-1]], position, self.size, margins, o_set, cards[floor(a/2)]) for a, position in enumerate(pos_list)]
        return self.played_cards

    def draw_card_screen(self, font, ui_images, m_pos, chosen_cards, background, pos_mod, choose_boolean):
        self.screen.blit(background, (0, pos_mod))
        if chosen_cards < 2:
            for card in self.played_cards:
                card.choose(m_pos, choose_boolean)
        for card in self.played_cards:
            card.draw(self.image_dict["card_back"], self.screen, pos_mod)
        self.draw_ui(ui_images, pos_mod, font)

    def draw_ui(self, ui_images, pos_mod, font):
        self.ui["surface"].fill((224, 255, 255, 200))
        self.screen.blit(self.ui["surface"], (self.ui["rect"].x, self.ui["rect"].y))
        pg.draw.rect(self.screen, cyan, self.ui["rect"], 5)
        for a in range(self.metadata["energy"]):
            if a < self.energy:
                x = self.ui["rect"].width / 2 - ui_images["energy_full"].get_rect().width / 2
                self.screen.blit(ui_images["energy_full"], (self.ui["rect"].x + x + (a - (self.metadata["energy"] - 1) / 2) * 75, self.ui["rect"].y + 10 + pos_mod))
            else:
                x = self.ui["rect"].width / 2 - ui_images["energy_empty"].get_rect().width / 2
                self.screen.blit(ui_images["energy_empty"], (self.ui["rect"].x + x + (a - (self.metadata["energy"] - 1) / 2) * 75, self.ui["rect"].y + 10 + pos_mod))
        m = [(a, self.buff_bar[a]) for a in self.buff_bar if self.buff_bar[a]] + [(a, self.status_bar[a]) for a in self.status_bar if self.status_bar[a]]
        size = (ui_images["status"]["Vulnerable"].get_rect().width, ui_images["status"]["Vulnerable"].get_rect().width)
        mod = ((self.ui["rect"].width - self.margins[0]) // (size[0] + self.margins[0]))
        for a, b in enumerate(m):
            i = self.ui["rect"].x + (a % mod) * (size[0] + self.margins[0]) + (self.ui["rect"].width - self.margins[0] * (mod - 1) - size[0] * mod) / 2
            j = self.ui["rect"].y + 100 + pos_mod + (size[1] + self.margins[1]) * (a // mod)
            self.screen.blit(ui_images["status" if b[0] in list(ui_images["status"].keys()) else "buff"][b[0]], (i, j))
            draw_text_right(str(b[1]), black, font, self.screen, i + size[0] + 10, j + size[1] + 10)

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
                                if self.attack["status"] == "None":
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
        self.block = self.attack["block"]
        damage += self.status_bar["Poison"]
        self.health += self.buff_bar["Regeneration"]
        self.health += self.attack["heal"]
        if self.health > self.metadata["hp"]:
            self.health = self.metadata["hp"]
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
