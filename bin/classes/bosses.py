import random

from abc import ABC, abstractmethod


class Boss(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_boss_info(self):
        pass

    @abstractmethod
    def act(self, turn_counter):
        pass

    @abstractmethod
    def update(self, damage):
        pass


class DevilChan(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.special = 0
        self.health = None
        self.energy = None
        self.attacks = None
        self.death = None
        self.block = 0
        self.special_move = None

    def load_boss_info(self):
        self.attacks = {b: self.metadata["boss"]["attacks"][a]
                        for (a, b) in (self.metadata["boss"]["attacks"], range(len(self.metadata["boss"]["attacks"]))) if "special" not in a and "death" not in a}
        self.special_move = self.metadata["boss"]["attacks"]["special"]
        self.death = self.metadata["boss"]["attacks"]["death"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move = self.attacks[turn_counter % (len(self.attacks - 1))]
        if self.health < self.metadata["hp"] // 2 and not self.special:
            move = self.special_move
            self.special = 1
        if self.health <= 0:
            move = self.death
        self.health += move[1][3]
        self.block += move[1][1]
        return move["phrases"][random.randint(0, len(move["phrases"] - 1))], move[1][0], move[1][2]

    def update(self, damage):
        self.energy = self.metadata["player"]["energy"]
        self.health -= damage


class MsG(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.death = None
        self.siberia_move = None
        self.block = 0
        self.siberia = False
        self.special_move = None

    def load_boss_info(self):
        self.attacks = {b: self.metadata["boss"]["attacks"][a]
                        for (a, b) in (self.metadata["boss"]["attacks"], range(len(self.metadata["boss"]["attacks"]))) if "special" not in a and "death" not in a}
        self.special_move = self.metadata["boss"]["attacks"]["special"]
        self.death = self.metadata["boss"]["attacks"]["death"]
        self.siberia_move = self.metadata["boss"]["attacks"]["siberia"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move = self.attacks[turn_counter % (len(self.attacks - 1))]
        if self.health == self.metadata["boss"]["hp"] and not self.siberia:
            move = self.special_move
            self.siberia = True
        elif self.health <= self.metadata["boss"]["hp"] // 2 and self.siberia:
            move = self.siberia_move
            self.siberia = False
        if self.health <= 0:
            move = self.death
        self.health += move[1][3]
        self.block += move[1][1]
        return move["phrases"][random.randint(0, len(move["phrases"] - 1))], move[1][0], move[1][2]

    def update(self, damage):
        self.energy = self.metadata["player"]["energy"]
        if self.siberia:
            self.energy -= 1
        self.health -= damage


class MrPhone(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.death = None
        self.block = 0
        self.special = 0
        self.damaged = True
        self.special_move = None

    def load_boss_info(self):
        self.attacks = {b: self.metadata["boss"]["attacks"][a]
                        for (a, b) in (self.metadata["boss"]["attacks"], range(len(self.metadata["boss"]["attacks"]))) if "special" not in a and "death" not in a}
        self.special_move = self.metadata["boss"]["attacks"]["special"]
        self.death = self.metadata["boss"]["attacks"]["death"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move = self.attacks[turn_counter % (len(self.attacks - 1))]
        if not self.damaged:
            move = self.special_move
            self.special = True
        if self.health <= 0:
            move = self.death
        self.health += move[1][3]
        self.block += move[1][1]
        return move["phrases"][random.randint(0, len(move["phrases"] - 1))], move[1][0], move[1][2]

    def update(self, damage):
        self.energy = self.metadata["player"]["energy"]
        self.damaged = False
        if damage:
            self.damaged = True
        self.health -= damage
