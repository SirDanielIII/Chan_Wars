from math import floor

import pygame as pg

from bin.blit_tools import *
from bin.colours import *

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
        self.margins = (20, 20)
        self.block = 0
        self.health = 0
        self.energy = 0
        self.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}}
        self.debuff_bar = {"fear": 0, "weakness": 0, "vulnerable": 0, "disappointment": 0, "wounded": 0, "marked": 0}
        self.buff_bar = {"power": 0, "lifesteal": 0, "regeneration": 0, "energized": 0, "armor": 0, "clairvoyant": 0}
        self.acted = False
        self.size = None
        self.choices = {}
        self.ui = {}
        self.deck = None
        self.intro_size = 20
        self.chosen_cards = []
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
        self.ui["rect"] = pg.Rect((X - (self.columns + 4.5) * self.size[0] - (self.columns - 1) * margins[0]) / 2, o_set[1], self.size[0] * 4,
                                  margins[1] * (self.rows - 1) + self.size[1] * self.rows)
        self.ui["surface"] = pg.Surface((self.size[0] * 4, margins[1] * (self.rows - 1) + self.size[1] * self.rows),
                                        flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        cards = random.sample(self.deck, int((self.columns * self.rows) / 2))
        pos_list = [(a, b) for a in range(self.columns) for b in range(self.rows)]
        random.shuffle(pos_list)
        self.played_cards = [Card(images[cards[floor(a / 2)].split()[-1]], position, self.size, margins, o_set, cards[floor(a / 2)]) for a, position in enumerate(pos_list)]
        return self.played_cards

    def draw_card_screen(self, effects_font, intro_font, ui_images, m_pos, chosen_cards, background, pos_mod, choose_boolean):
        self.screen.blit(background, (0, pos_mod))
        if chosen_cards < 2:
            for card in self.played_cards:
                card.choose(m_pos, choose_boolean)
        for card in self.played_cards:
            card.draw(self.image_dict["card_back"], self.screen, pos_mod)
        self.draw_ui(ui_images, pos_mod, effects_font, intro_font)

    def draw_ui(self, ui_images, pos_mod, effects_font, intro_font):
        self.ui["surface"].fill((224, 255, 255, 200))
        self.screen.blit(self.ui["surface"], (self.ui["rect"].x, self.ui["rect"].y))
        pg.draw.rect(self.screen, cyan, self.ui["rect"], 5)
        # ------------------------------------------------------------------------------------------------------------------
        # Energy
        for a in range(self.metadata["energy"]):
            if a < self.energy:
                x = self.ui["rect"].width / 2 - ui_images["energy_full"].get_rect().width / 2
                self.screen.blit(ui_images["energy_full"], (self.ui["rect"].x + x + (a - (self.metadata["energy"] - 1) / 2) * 75, self.ui["rect"].y + 10))
            else:
                x = self.ui["rect"].width / 2 - ui_images["energy_empty"].get_rect().width / 2
                self.screen.blit(ui_images["energy_empty"], (self.ui["rect"].x + x + (a - (self.metadata["energy"] - 1) / 2) * 75, self.ui["rect"].y + 10))
        # ------------------------------------------------------------------------------------------------------------------
        # Status Effects
        self.debuff_bar = {"fear": 1, "weakness": 1, "vulnerable": 1, "disappointment": 1, "wounded": 1, "marked": 1}
        self.buff_bar = {"power": 1, "lifesteal": 1, "regeneration": 1, "energized": 1, "armor": 1, "clairvoyant": 1}
        m = [(a, self.buff_bar[a]) for a in self.buff_bar if self.buff_bar[a]] + [(a, self.debuff_bar[a]) for a in self.debuff_bar if self.debuff_bar[a]]
        size = (ui_images["debuff"]["vulnerable"].get_rect().width, ui_images["debuff"]["vulnerable"].get_rect().width)
        mod = ((self.ui["rect"].width - self.margins[0]) // (size[0] + self.margins[0]))
        for a, b in enumerate(m):
            i = self.ui["rect"].x + (a % mod) * (size[0] + self.margins[0]) + (self.ui["rect"].width - self.margins[0] * (mod - 1) - size[0] * mod) / 2
            j = self.ui["rect"].y + 95 + pos_mod + (size[1] + self.margins[1]) * (a // mod)
            self.screen.blit(ui_images["debuff" if b[0].lower() in list(ui_images["debuff"].keys()) else "buff"][b[0].lower()], (i, j))
            draw_text_right(str(b[1]), black, effects_font, self.screen, i + size[0] + 10, j + size[1] + 10)
        # ------------------------------------------------------------------------------------------------------------------
        # Block
        self.screen.blit(ui_images["block"], (self.ui["rect"].x + 20, 270))
        draw_text_left(str(self.block) + " Block", black, effects_font, self.screen, self.ui["rect"].x + 65, 275)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Overview
        for a, card in enumerate(self.chosen_cards):
            self.screen.blit(pg.transform.smoothscale(self.image_dict[card], (150, 225)).convert_alpha(), (self.ui["rect"].x + 20, a * 250 + 325))
            draw_text_left(card[0].upper() + card[1:-5] + " " + card[-4].upper() + card[-3:], black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325)
            draw_text_left("> Damage: " + str(self.cards[card]["damage"]), black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + self.intro_size)
            draw_text_left("> Block: " + str(self.cards[card]["block"]), black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + 2 * self.intro_size)
            draw_text_left("> Heal: " + str(self.cards[card]["heal"]), black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + 3 * self.intro_size)
            draw_text_left("> Buff: " + str(self.cards[card]["buff"]), black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + 4 * self.intro_size)
            draw_text_left("> Debuff: " + str(self.cards[card]["debuff"]), black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + 5 * self.intro_size)
            draw_text_left("> Upgrades: ", black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + 6 * self.intro_size)
            for m, n in enumerate(self.cards[card]["upgrades"].keys()):
                draw_text_left("  > " + str(n), black, intro_font, self.screen, self.ui["rect"].x + 180, a * 250 + 325 + (m + 7) * self.intro_size)

    def complete(self):
        count = 0
        self.choices = {}
        for a in self.played_cards:
            self.choices[a.card_type] = self.choices.get(a.card_type, 0)
            self.choices[a.card_type] += a.chosen
            if a.chosen and a.card_type.split()[-1] not in self.chosen_cards:
                self.chosen_cards.insert(0, a.card_type.split()[-1])
                if len(self.chosen_cards) > 2:
                    self.chosen_cards = self.chosen_cards[:2]
        for card_type, number in self.choices.items():
            if number == 2 and not self.acted:
                card = card_type.split(" ")
                mod = 1
                if self.debuff_bar["weakness"]:
                    mod *= 0.75
                if self.buff_bar["power"]:
                    mod *= 1.25
                self.attack["damage"] += self.cards[card[-1]]["damage"] * mod
                self.attack["block"] += self.cards[card[-1]]["block"]
                self.attack["heal"] += self.cards[card[-1]]["heal"]
                if self.cards[card[-1]]["debuff"] != "None":
                    for debuff in self.cards[card[-1]]["debuff"]:
                        self.attack["debuff"][debuff] = self.attack["debuff"].get(debuff, 0)
                        self.attack["debuff"][debuff] += self.cards[card[-1]]["debuff"][debuff]
                if self.cards[card[-1]]["buff"] != "None":
                    for buff in self.cards[card[-1]]["buff"]:
                        self.attack["buff"][buff] = self.attack["buff"].get(buff, 0)
                        self.attack["buff"][buff] += self.cards[card[-1]]["buff"][buff]
                if len(card) > 1:
                    for upgrade in card[:-1]:
                        self.attack["damage"] += self.cards[card[-1]]["upgrades"][upgrade]["damage"]
                        self.attack["block"] += self.cards[card[-1]]["upgrades"][upgrade]["block"]
                        self.attack["heal"] += self.cards[card[-1]]["upgrades"][upgrade]["heal"]
                        if self.cards[card[-1]]["upgrades"][upgrade]["debuff"] != "None":
                            for debuff in self.cards[card[-1]]["upgrades"][upgrade]["debuff"]:
                                if self.attack["debuff"] == "None":
                                    self.attack["debuff"] = {debuff: self.cards[card[-1]]["upgrades"][upgrade]["debuff"][debuff]}
                                else:
                                    self.attack["debuff"][debuff] = self.attack["debuff"].get(debuff, 0)
                                    self.attack["debuff"][debuff] += self.cards[card[-1]]["upgrades"][upgrade]["debuff"][debuff]
                        if self.cards[card[-1]]["upgrades"][upgrade]["buff"] != "None":
                            for buff in self.cards[card[-1]]["upgrades"][upgrade]["buff"]:
                                if self.attack["buff"] == "None":
                                    self.attack["buff"] = {buff: self.cards[card[-1]]["upgrades"][upgrade]["buff"][buff]}
                                else:
                                    self.attack["buff"][buff] = self.attack["buff"].get(buff, 0)
                                    self.attack["buff"][buff] += self.cards[card[-1]]["upgrades"][upgrade]["buff"][buff]
                if self.buff_bar["lifesteal"]:
                    self.attack["heal"] += self.attack["damage"]
                self.block += self.attack["block"] - self.block
                self.acted = True
                return 2, self.attack["damage"], self.attack["debuff"]
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

    def update(self, damage, debuff):
        self.energy = self.metadata["energy"]
        self.energy += self.buff_bar["energized"]
        if self.buff_bar["armor"]:
            self.block += self.buff_bar["armor"]
        if self.debuff_bar["vulnerable"]:
            damage *= 1.25
        if self.debuff_bar["marked"] and damage:
            damage += self.debuff_bar["marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.debuff_bar["wounded"]
        self.health += self.buff_bar["regeneration"]
        self.health += self.attack["heal"]
        if self.health > self.metadata["hp"]:
            self.health = self.metadata["hp"]
        if self.health > self.metadata["hp"]:
            self.health = self.metadata["hp"]
        self.health -= damage
        for a in self.debuff_bar:
            if self.debuff_bar[a]:
                self.debuff_bar[a] -= 1
        for b in self.buff_bar:
            if self.buff_bar[b]:
                self.buff_bar[b] -= 1
        if debuff != "None":
            for effect in debuff:
                self.debuff_bar[effect] += debuff[effect]
        if self.attack["buff"] != "None":
            for buff in self.attack["buff"]:
                self.buff_bar[buff] += self.attack["buff"][buff]
