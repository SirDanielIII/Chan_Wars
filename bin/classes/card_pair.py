import random
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


class CardPair(object):
    def __init__(self, image, pos, size, m, columns, o_set, card_type):
        self.size = size
        self.position1 = [o_set[0] - columns + (size[0] + m[0]) * pos[0][0],
                          o_set[1] + (size[1] + m[1]) * pos[0][1]]
        self.position2 = [o_set[0] - columns + (size[0] + m[0]) * pos[1][0],
                          o_set[1] + (size[1] + m[1]) * pos[1][1]]
        self.image = image
        self.chosen1 = 0
        self.chosen2 = 0
        self.card_type = card_type

    def choose(self, m_pos, choose_boolean, rect_pair):
        if choose_boolean:
            if rect_pair[0].collidepoint(m_pos):
                self.chosen1 = 1
            if rect_pair[1].collidepoint(m_pos):
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
    def __init__(self, screen, config):
        self.screen = screen
        self.metadata = config
        self.rows = 0
        self.cards = None
        self.columns = 0
        self.image_dict = None
        self.damage = 0
        self.block = 0
        self.health = 0
        self.energy = 0
        self.attack = []
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Energized": 0, "Armor": 0, "Clairvoyant": 0}
        self.set = []
        self.acted = False

    def initialize(self, image_dict):
        self.rows = self.metadata["rows"]
        self.cards = self.metadata["cards"]
        self.columns = self.metadata["columns"]
        self.image_dict = image_dict
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]


    def generate_pairs(self, size, margins, X, Y):
        # ------------------------------------------------------------------------------------------------------------------
        o_set = ((X - (margins[0] + size[0]) * self.columns) / 2, (Y - (margins[1] + size[1]) * 4) / 2)
        # Daniel made it so that the offset was calculated in the method and not in the parameters
        image_collection = random.sample([a for a in range(self.rows * self.columns)], self.rows * self.columns)
        pos_list = [(a, b, image_collection.pop(-1)) for a in range(self.columns) for b in range(self.rows)]
        card_set = [CardPair(self.image_dict[card1[2] // 2][0], ((card1[:2]), (card2[:2])), size, margins, self.columns, o_set, self.image_dict[card1[2] // 2][1])
                    for card1 in pos_list for card2 in pos_list if card1[2] + 1 == card2[2] and card2[2] % 2]
        rect_set = [(pg.Rect(card_pair.position1[0], card_pair.position1[1], card_pair.size[0], card_pair.size[1]),
                     pg.Rect(card_pair.position2[0], card_pair.position2[1], card_pair.size[0], card_pair.size[1])) for card_pair in card_set]
        self.set = [(card_set[i], rect_set[i]) for i in range(len(rect_set))]
        # Here Daniel unified the card set and the rect set to make sure that neither order spontaneously changed while the program ran
        return self.set

    def draw_cards(self, m_pos, chosen_cards, background, pos_mod, choose_boolean):
        self.screen.blit(background, (0, pos_mod))
        if chosen_cards < 2:
            for pair in self.set:
                pair[0].choose(m_pos, choose_boolean, pair[1])
        for pair in [cards[0] for cards in self.set]:
            pair.draw_matching(self.image_dict["card_back"], self.screen, pos_mod)

    def complete(self):
        count = 0
        for a in self.set:
            if a[0].chosen1 + a[0].chosen2 == 2 and not self.acted:
                attack = self.cards[a[0].card_type]
                if attack["buff"] != "None":
                    self.buff_bar[attack["buff"][0]] += attack["buff"][1]
                if self.buff_bar["Lifesteal"]:
                    attack["heal"] += attack["damage"]
                if self.buff_bar["Armor"]:
                    attack["block"] += self.buff_bar["Armor"]
                if self.status_bar["Weakness"]:
                    attack["damage"] *= 0.75
                if self.buff_bar["Power"]:
                    attack["damage"] *= 1.25
                self.health += attack["heal"]
                if self.health > self.metadata["hp"]:
                    self.health = self.metadata["hp"]
                self.block = attack["block"]
                self.acted = True
                print(self.status_bar, self.buff_bar, attack)
                return 2, attack["damage"], attack["status"]
            else:
                count += a[0].chosen1 + a[0].chosen2
        if count == 2:
            self.acted = True
        return count, 0, "None"

    def reset(self):
        for m, a in enumerate(self.set):
            if a[0].chosen1 + a[0].chosen2 == 2:
                self.set.pop(m)
            a[0].chosen1 = 0
            a[0].chosen2 = 0
        self.acted = False

    def update(self, damage, status_effects):
        print(self.status_bar, self.buff_bar)
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
            self.status_bar[status_effects[0]] += status_effects[1]
