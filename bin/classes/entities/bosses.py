import random

from abc import ABC, abstractmethod


class Boss(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self):
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
        self.status_bar = {"Weakness": 0, "Vulnerable": 0, "Disappointment": 0, "Pained": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Armor": 0}
        self.moves = None
        self.images = {"background": None, "face": None}
        self.block = 0
        self.move = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}}
        self.phrases = None

    def initialize(self):
        self.moves = {b: self.metadata["moves"][b] for b in self.metadata["moves"] if "basic" in b}
        self.phrases = self.metadata["phrases"]
        self.moves["special"] = self.metadata["moves"]["special"]
        self.health = self.metadata["hp"]

    def act(self, turn_counter):
        move_type = "basic"
        move = self.moves[move_type][(turn_counter % (len(self.moves["basic"]) - 1))]
        if self.health < self.metadata["hp"] // 2 and not self.special:
            move_type = "special"
            self.special = 1
            move = self.moves[move_type]
        print(move)
        mod = 1
        if self.status_bar["Weakness"]:
            mod *= 0.75
        if self.buff_bar["Power"]:
            mod *= 1.25
        self.move["damage"] += move["damage"] * mod
        self.move["block"] += move["block"]
        self.move["heal"] += move["heal"]
        if move["status"] != "None":
            for status in move["status"]:
                self.move["status"][status] = self.move["status"].get(status, 0)
                self.move["status"][status] += move["status"][status]
        if move["buff"] != "None":
            for buff in move["buff"]:
                self.move["buff"][buff] = self.move["buff"].get(buff, 0)
                self.move["buff"][buff] += move["buff"][buff]
        if self.buff_bar["Lifesteal"]:
            self.move["heal"] += self.move["damage"]
        if self.buff_bar["Armor"]:
            self.move["block"] += self.buff_bar["Armor"]
        if self.status_bar["Weakness"]:
            self.move["damage"] *= 0.75
        if self.buff_bar["Power"]:
            self.move["damage"] *= 1.25
        self.health += self.move["heal"]
        self.block += self.move["block"]
        return move_type

    def update(self, damage, status_effects):
        if self.status_bar["Vulnerable"]:
            damage *= 1.25
        if self.status_bar["Marked"] and damage:
            damage += self.status_bar["Marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.status_bar["Pained"]
        self.health += self.buff_bar["Regeneration"]
        self.health -= damage
        if status_effects != "None":
            for effect in status_effects:
                self.status_bar[effect] += status_effects[effect]
        if self.move["buff"] != "None":
            for buff in self.move["buff"]:
                self.buff_bar[buff] += self.move["buff"][buff]


class MsG(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.special = 0
        self.health = None
        self.status_bar = {"Weakness": 0, "Vulnerable": 0, "Disappointment": 0, "Pained": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Armor": 0}
        self.moves = None
        self.images = {"background": None, "face": None}
        self.block = 0
        self.phrases = None
        self.siberia = False

    def initialize(self):
        self.moves = {b: self.metadata["moves"][b] for b in self.metadata["moves"] if "basic" in b}
        self.moves["special"] = self.metadata["moves"]["special"]
        self.moves["siberia"] = self.metadata["moves"]["siberia"]
        self.phrases = self.metadata["phrases"]
        self.health = self.metadata["hp"]

    def act(self, turn_counter):
        move_type = "basic_" + str((turn_counter % (len(self.moves) - 2)) + 1)
        move = self.moves[move_type]
        if turn_counter == 0:
            move_type = "special"
            move = self.moves["special"]
            self.siberia = True
        elif self.health <= self.metadata["hp"] // 2 and self.siberia:
            move_type = "special"
            move = self.moves["siberia"]
            self.siberia = False
        if self.buff_bar["Lifesteal"]:
            move["heal"] += move["damage"]
        if self.buff_bar["Armor"]:
            move["block"] += self.buff_bar["Armor"]
        if self.status_bar["Weakness"]:
            move["damage"] *= 0.75
        if self.buff_bar["Power"]:
            move["damage"] *= 1.25
        self.health += move["heal"]
        self.block += move["block"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        if self.status_bar["Vulnerable"]:
            damage *= 1.25
        if self.status_bar["Marked"] and damage:
            damage += self.status_bar["Marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.status_bar["Pained"]
        self.health += self.buff_bar["Regeneration"]
        self.health -= damage
        for effect in status_effects:
            if effect != "None":
                self.status_bar[effect] += status_effects[effect]


class MrPhone(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.special = 0
        self.health = None
        self.status_bar = {"Weakness": 0, "Vulnerable": 0, "Disappointment": 0, "Pained": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Armor": 0}
        self.moves = None
        self.images = {"background": None, "face": None}
        self.block = 0
        self.phrases = None
        self.damaged = True

    def initialize(self):
        self.moves = {b: self.metadata["moves"][b] for b in self.metadata["moves"] if "basic" in b}
        self.moves["special"] = self.metadata["moves"]["special"]
        self.phrases = self.metadata["phrases"]
        self.health = self.metadata["hp"]

    def act(self, turn_counter):
        move_type = "basic_" + str((turn_counter % (len(self.moves) - 2)) + 1)
        move = self.moves[move_type]
        if not self.damaged:
            move_type = "special"
            move = self.moves["special"]
            self.special = True
        if self.buff_bar["Lifesteal"]:
            move["heal"] += move["damage"]
        if self.buff_bar["Armor"]:
            move["block"] += self.buff_bar["Armor"]
        if self.status_bar["Weakness"]:
            move["damage"] *= 0.75
        if self.buff_bar["Power"]:
            move["damage"] *= 1.25
        self.health += move["heal"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        self.block += move["block"]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        if self.status_bar["Vulnerable"]:
            damage *= 1.25
        if self.status_bar["Marked"] and damage:
            damage += self.status_bar["Marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.status_bar["Pained"]
        self.health += self.buff_bar["Regeneration"]
        self.health -= damage
        self.damaged = False
        if damage:
            self.damaged = True
        for action in status_effects:
            if action != "None":
                for effect in action:
                    self.status_bar[effect] += action[effect]
