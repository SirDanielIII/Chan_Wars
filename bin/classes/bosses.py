import random
import math
import pygame as pg
from abc import ABC, abstractmethod


class Boss(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def trigger(self):
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
    def __init__(self, surface, config):
        super().__init__()
        self.screen = surface
        self.metadata = config["DevilChan"]
        self.trigger = None
        self.acting = True  # Whether or not it's the boss's turn
        self.time = 0
        self.pos_mod = 50 * math.sin(self.time)
        self.special = 0
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]
        self.basic_power = self.metadata["basic"][1]
        self.attack_phrases = self.metadata["phrases"]["attack"]

    def update(self, damage, time, boss_turn):
        self.health -= damage
        self.acting = boss_turn
        self.time = time
        self.energy = self.metadata["energy"]
        self.pos_mod = 50 * math.sin(time)
        return self.health, self.energy, self.pos_mod

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if self.health < self.metadata["hp"] // 2 and not self.special:
                self.trigger = "special"
            if self.health <= 0:
                self.trigger = "die"

    def act(self):
        if self.acting:
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
        self.update(0, pg.time.get_ticks(), True)
        return self.metadata["special"][1], self.metadata["phrases"]["special"][random.randint(0, len(self.metadata["phrases"]["special"]) - 1)]


class MsG(Boss):
    def __init__(self, surface, config):
        super().__init__()
        self.screen = surface
        self.metadata = config["MsG"]
        self.trigger = None
        self.acting = True  # Whether or not it's the boss's turn
        self.time = 0
        self.pos_mod = 50 * math.sin(self.time)
        self.special = 0
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]
        self.basic_power = self.metadata["basic"][1]
        self.attack_phrases = self.metadata["phrases"]["attack"]
        self.siberia = False

    def update(self, damage, time, boss_turn):
        self.health -= damage
        self.acting = boss_turn
        if self.siberia:
            self.energy = self.metadata["energy"] - 1
        else:
            self.energy = self.metadata["energy"]
        return self.health, self.energy, self.siberia

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if self.health != self.metadata["hp"] and self.health > self.metadata["hp"] // 2:
                self.special = 0
            if (self.health == self.metadata["hp"] and not self.special) or (self.health <= self.metadata["hp"] // 2 and not self.special):
                self.trigger = "special"
            if self.health <= 0:
                self.trigger = "die"

    def act(self):
        if self.acting:
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
        if self.health > self.metadata["hp"] // 2:
            self.special = 1
            self.siberia = self.metadata["special"][1]
            return self.siberia, self.metadata["phrases"]["special"][random.randint(0, len(self.metadata["phrases"]["special"]) - 1)]
        else:
            self.special = 1
            self.siberia = False
            return self.siberia, self.metadata["phrases"]["special"]["out"]


class MrPhone(Boss):
    def __init__(self, surface, config):
        super().__init__()
        self.screen = surface
        self.metadata = config["DevilChan"]
        self.trigger = None
        self.acting = True  # Whether or not it's the boss's turn
        self.time = 0
        self.pos_mod = 50 * math.sin(self.time)
        self.special = 0
        self.health = self.metadata["hp"]
        self.energy = self.metadata["energy"]
        self.basic_power = self.metadata["basic"][1]
        self.attack_phrases = self.metadata["phrases"]["attack"]
        self.damaged = True
        self.turn_count = 1

    def update(self, damage, turn_counter, time, boss_turn):
        self.health -= damage
        self.acting = boss_turn
        self.damaged = False
        if damage:
            self.damaged = True
        self.turn_count = turn_counter
        self.energy = self.metadata["energy"]
        return self.health, self.energy

    def trigger(self):
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
