import random
import os
import pygame as pg

from abc import ABC, abstractmethod
from bin.classes.level import Level


def redraw_screen(surface, background=None):
    pg.display.update()
    surface.fill((255, 255, 255))
    if background:
        surface.blit(background, (0, 0))


class Boss(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_boss_info(self):
        pass

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def trigger_method(self):
        pass

    @abstractmethod
    def death(self):
        pass

    @abstractmethod
    def basic_action(self):
        pass

    @abstractmethod
    def special_action(self):
        pass


class DevilChan(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.trigger = None
        self.special = 0
        self.health = None
        self.energy = None
        self.basic_power = None
        self.attack_phrases = None

    def load_boss_info(self):
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]
        self.basic_power = self.metadata["basic"][1]
        self.attack_phrases = self.metadata["phrases"]["attack"]

    def update(self, damage):
        self.health -= damage
        self.energy = self.metadata["energy"]

    def trigger_method(self):
        self.trigger = "attack"
        if self.health < self.metadata["hp"] // 2 and not self.special:
            self.trigger = "special"
        if self.health <= 0:
            self.trigger = "die"

    def act(self):
        match self.trigger:
            case "attack":
                return self.trigger, self.basic_action()
            case "die":
                return self.trigger, self.death()
            case "special":
                return self.trigger, self.special_action()

    def death(self):
        return self.metadata["phrases"]["death"]

    def basic_action(self):
        return self.basic_power, self.attack_phrases[random.randint(0, len(self.attack_phrases) - 1)]

    def special_action(self):
        self.health += self.metadata["special"][2]
        self.special = 1
        self.update(0)
        return self.metadata["special"][1], self.metadata["phrases"]["special"][random.randint(0, len(self.metadata["phrases"]["special"]) - 1)]


class MsG(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.trigger = None
        self.special = 0
        self.health = None
        self.energy = None
        self.basic_power = None
        self.attack_phrases = None
        self.siberia = False

    def load_boss_info(self):
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]
        self.basic_power = self.metadata["basic"][1]
        self.attack_phrases = self.metadata["phrases"]["attack"]

    def update(self, damage):
        self.health -= damage
        if self.siberia:
            self.energy = self.metadata["energy"] - 1
        else:
            self.energy = self.metadata["energy"]

    def trigger_method(self):
        self.trigger = "attack"
        if (self.health == self.metadata["hp"] and not self.special) or (self.health <= self.metadata["hp"] // 2 and self.siberia):
            self.trigger = "special"
        if self.health <= 0:
            self.trigger = "die"

    def act(self):
        match self.trigger:
            case "attack":
                return self.trigger, self.basic_action()
            case "die":
                return self.trigger, self.death()
            case "special":
                return self.trigger, self.special_action()

    def death(self):
        return self.metadata["phrases"]["death"], "death"

    def basic_action(self):
        return self.basic_power, self.attack_phrases[random.randint(0, len(self.attack_phrases) - 1)], "normal"

    def special_action(self):
        if not self.siberia:
            self.special = 1
            self.siberia = True
            return self.siberia, self.metadata["phrases"]["special"][random.randint(0, len(self.metadata["phrases"]["special"]) - 1)], "siberia-01"
        else:
            self.special = 1
            self.siberia = False
            return self.siberia, self.metadata["phrases"]["special"], "siberia-02"
            # ["out"]


class MrPhone(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config["MrPhone"]
        self.trigger = None
        self.acting = True  # Whether or not it's the boss's turn
        self.special = 0
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]
        self.basic_power = self.metadata["basic"][1]
        self.attack_phrases = self.metadata["phrases"]["attack"]
        self.damaged = True
        self.turn_count = 1

    def update(self, damage, turn_counter, boss_turn):
        self.health -= damage
        self.acting = boss_turn
        self.damaged = False
        if damage:
            self.damaged = True
        self.turn_count = turn_counter
        self.energy = self.metadata["energy"]
        return self.health, self.energy

    def trigger_method(self):
        if self.acting:
            self.trigger = "attack"
            if not self.turn_count % 4:
                self.trigger = "special"
            if not self.damaged:
                self.trigger = "kill"
            if self.health <= 0:
                self.trigger = "die"

    def act(self):
        match self.trigger:
            case "attack":
                return self.trigger, self.basic_action()
            case "die":
                return self.trigger, self.death()
            case "special":
                return self.trigger, self.special_action()
            case "kill":
                return self.trigger, self.kill()

    def kill(self):
        return self.metadata["kill"][1], self.metadata["phrases"]["kill"][random.randint(0, len(self.metadata["phrases"]["kill"]) - 1)]

    def death(self):
        return self.metadata["phrases"]["death"]

    def basic_action(self):
        return self.basic_power, self.attack_phrases[random.randint(0, len(self.attack_phrases) - 1)]

    def special_action(self):
        return self.metadata["special"][1], self.metadata["phrases"]["special"][random.randint(0, len(self.metadata["phrases"]["special"]) - 1)]
