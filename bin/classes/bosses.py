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
        self.moves = None
        self.death = None
        self.block = 0
        self.special_move = None
        self.phrases = None

    def load_boss_info(self):
        self.moves = {a: self.metadata["boss"]["moves"][b] for a, b in enumerate(self.metadata["boss"]["moves"]) if "special" not in b and "death" not in b}
        self.phrases = self.metadata["boss"]["phrases"]
        self.special_move = self.metadata["boss"]["moves"]["special"]
        self.death = self.metadata["boss"]["moves"]["death"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[(turn_counter - 1) % (len(self.moves) - 1)]
        if self.health < self.metadata["hp"] // 2 and not self.special:
            move_type = "special"
            move = self.special_move
            self.special = 1
        if self.health <= 0:
            move_type = "death"
            move = self.death
        self.health += move["heal"]
        self.block += move["block"]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage):
        self.energy = self.metadata["player"]["energy"]
        self.health -= damage


class MsG(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.moves = None
        self.death = None
        self.siberia_move = None
        self.block = 0
        self.siberia = False
        self.phrases = None
        self.special_move = None

    def load_boss_info(self):
        self.moves = {a: self.metadata["boss"]["moves"][b] for a, b in enumerate(self.metadata["boss"]["moves"]) if "special" not in b and "death" not in b}
        self.phrases = self.metadata["boss"]["phrases"]
        self.special_move = self.metadata["boss"]["moves"]["special"]
        self.death = self.metadata["boss"]["moves"]["death"]
        self.siberia_move = self.metadata["boss"]["moves"]["siberia"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[(turn_counter - 1) % (len(self.moves) - 1)]
        if turn_counter == 0:
            move_type = "special"
            move = self.special_move
            self.siberia = True
        elif self.health <= self.metadata["boss"]["hp"] // 2 and self.siberia:
            move_type = "special"
            move = self.siberia_move
            self.siberia = False
        if self.health <= 0:
            move_type = "death"
            move = self.death
        self.health += move["heal"]
        self.block += move["block"]
        print(move, self.moves, turn_counter)
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

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
        self.moves = None
        self.death = None
        self.block = 0
        self.special = 0
        self.damaged = True
        self.special_move = None
        self.phrases = None

    def load_boss_info(self):
        self.moves = {a: self.metadata["boss"]["moves"][b] for a, b in enumerate(self.metadata["boss"]["moves"]) if "special" not in b and "death" not in b}
        self.special_move = self.metadata["boss"]["moves"]["special"]
        self.phrases = self.metadata["boss"]["phrases"]
        self.death = self.metadata["boss"]["moves"]["death"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[(turn_counter - 1) % (len(self.moves) - 1)]
        if not self.damaged:
            move_type = "special"
            move = self.special_move
            self.special = True
        if self.health <= 0:
            move_type = "death"
            move = self.death
        self.health += move["heal"]
        self.block += move["block"]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage):
        self.energy = self.metadata["player"]["energy"]
        self.damaged = False
        if damage:
            self.damaged = True
        self.health -= damage
