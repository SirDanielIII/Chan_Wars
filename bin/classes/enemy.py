import random

from abc import ABC, abstractmethod


class Enemy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initialize_type(self):
        pass

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def update(self, damage, turn_counter=0):
        pass

    @abstractmethod
    def death(self):
        pass

    @abstractmethod
    def basic_action(self):
        pass


class FlyingChan(Enemy):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.name = None

    def initialize_type(self):
        self.name = "flying"
        self.attacks = {a: "{} used {}".format(self.metadata["enemies"][self.name]["name"], a["phrase"])
                        for a in self.metadata["enemies"]["attacks"]}
        self.health = self.metadata["enemies"][self.name]["health"]
        self.energy = self.metadata["boss"]["energy"]

    def act(self):
        pass

    def update(self, damage, turn_counter=0):
        pass

    def death(self):
        pass

    def basic_action(self):
        pass
