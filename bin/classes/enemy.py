import random


class Enemy:
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.block = 0
        self.name = None

    def initialize_type(self, name):
        self.name = name
        self.attacks = {b: self.metadata["enemies"][self.name]["attacks"][a]
                        for (a, b) in (self.metadata["enemies"][self.name]["attacks"], range(len(self.metadata["enemies"][self.name]["attacks"])))}
        self.health = self.metadata["enemies"][self.name]["health"]
        self.energy = self.metadata["boss"]["energy"]

    def act(self, turn_counter):
        attack = self.attacks[str(turn_counter % (len(self.attacks - 1)))]
        self.health += attack["heal"]
        self.block += attack["block"]
        phrase = "{} used {}".format(self.metadata["enemies"][self.name]["name"], attack["phrase"])
        return phrase, attack["damage"], attack["status"]
