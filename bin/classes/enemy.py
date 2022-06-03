import random

from abc import ABC, abstractmethod


class Enemy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initialize_type(self):
        pass

    @abstractmethod
    def act(self, turn_counter):
        pass


class FlyingChan(Enemy):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.block = 0
        self.name = None

    def initialize_type(self):
        self.name = "flying"
        self.attacks = {b: ("{} used {}".format(self.metadata["enemies"][self.name]["name"], a["phrase"]), (a["damage"], a["block"], a["status"], a["heal"]))
                        for (a, b) in (self.metadata["enemies"]["attacks"], range(len(self.metadata["enemies"]["attacks"])))}
        self.health = self.metadata["enemies"][self.name]["health"]
        self.energy = self.metadata["boss"]["energy"]

    def act(self, turn_counter):
        attack = self.attacks[turn_counter % (len(self.attacks - 1))]
        self.health += attack[1][3]
        self.block += attack[1][1]
        return attack[0], attack[1][0], attack[1][2]
