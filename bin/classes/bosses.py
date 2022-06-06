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
    def update(self, damage, status_effects):
        pass


class DevilChan(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.special = 0
        self.health = None
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0}
        self.buff_bar = {"Power": 0, "Regeneration": 0, "Dodge": 0, "Armor": 0, "Clairvoyant": 0}
        self.energy = None
        self.moves = None
        self.images = {"background": None, "face": None}
        self.block = 0
        self.phrases = None

    def load_boss_info(self):
        self.moves = {a: self.metadata["boss"]["moves"][b] for a, b in enumerate(self.metadata["boss"]["moves"]) if "basic" in b}
        self.phrases = self.metadata["boss"]["phrases"]
        self.moves["special"] = self.metadata["boss"]["moves"]["special"]
        self.moves["death"] = self.metadata["boss"]["moves"]["death"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[turn_counter % (len(self.moves) - 2)]
        if self.health < self.metadata["hp"] // 2 and not self.special:
            move_type = "special"
            move = self.moves["special"]
            self.special = 1
        if self.health <= 0:
            move_type = "death"
            move = self.moves["death"]
        self.health += move["heal"]
        self.block += move["block"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        self.energy = self.metadata["player"]["energy"]
        self.health -= damage - self.block
        self.block = 0 if self.block < damage else self.block - damage
        if status_effects != "None":
            self.status_bar[status_effects[0]] += status_effects[1]


class MsG(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.moves = None
        self.block = 0
        self.siberia = False
        self.phrases = None
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0}
        self.buff_bar = {"Power": 0, "Regeneration": 0, "Dodge": 0, "Armor": 0, "Clairvoyant": 0}

    def load_boss_info(self):
        self.moves = {a: self.metadata["boss"]["moves"][b] for a, b in enumerate(self.metadata["boss"]["moves"]) if "basic" in b}
        self.moves["special"] = self.metadata["boss"]["moves"]["special"]
        self.moves["siberia"] = self.metadata["boss"]["moves"]["siberia"]
        self.moves["death"] = self.metadata["boss"]["moves"]["death"]
        self.phrases = self.metadata["boss"]["phrases"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[turn_counter % (len(self.moves) - 3)]
        print(turn_counter, move, self.moves, len(self.moves))
        if turn_counter == 0:
            move_type = "special"
            move = self.moves["special"]
            self.siberia = True
        elif self.health <= self.metadata["boss"]["hp"] // 2 and self.siberia:
            move_type = "special"
            move = self.moves["siberia"]
            self.siberia = False
        if self.health <= 0:
            move_type = "death"
            move = self.moves["death"]
        self.health += move["heal"]
        self.block += move["block"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        self.energy = self.metadata["player"]["energy"]
        if self.siberia:
            self.energy -= 1
        self.health -= damage - self.block
        self.block = 0 if self.block < damage else self.block - damage
        if status_effects != "None":
            self.status_bar[status_effects[0]] += status_effects[1]


class MrPhone(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.moves = None
        self.block = 0
        self.special = 0
        self.damaged = True
        self.phrases = None
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0}
        self.buff_bar = {"Power": 0, "Regeneration": 0, "Dodge": 0, "Armor": 0, "Clairvoyant": 0}

    def load_boss_info(self):
        self.moves = {a: self.metadata["boss"]["moves"][b] for a, b in enumerate(self.metadata["boss"]["moves"]) if "basic" in b}
        self.moves["special"] = self.metadata["boss"]["moves"]["special"]
        self.moves["death"] = self.metadata["boss"]["moves"]["death"]
        self.phrases = self.metadata["boss"]["phrases"]
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[turn_counter % (len(self.moves) - 2)]
        if not self.damaged:
            move_type = "special"
            move = self.moves["special"]
            self.special = True
        if self.health <= 0:
            move_type = "death"
            move = self.moves["death"]
        self.health += move["heal"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        self.block += move["block"]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        self.energy = self.metadata["player"]["energy"]
        self.damaged = False
        if damage:
            self.damaged = True
        self.health -= damage - self.block
        self.block = 0 if self.block < damage else self.block - damage
        if status_effects != "None":
            self.status_bar[status_effects[0]] += status_effects[1]
