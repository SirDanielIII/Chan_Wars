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
    def update(self, damage, debuff):
        pass


class DevilChan(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.special = 0
        self.health = None
        self.debuff_bar = {"weakness": 0, "vulnerable": 0, "disappointment": 0, "wounded": 0, "marked": 0}
        self.buff_bar = {"power": 0, "lifesteal": 0, "regeneration": 0, "armor": 0}
        self.moves = None
        self.images = {"background": None, "face": None}
        self.block = 0
        self.move = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}}
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
        if self.debuff_bar["weakness"]:
            mod *= 0.75
        if self.buff_bar["power"]:
            mod *= 1.25
        self.move["damage"] += move["damage"] * mod
        self.move["block"] += move["block"]
        self.move["heal"] += move["heal"]
        if move["debuff"] != "None":
            for debuff in move["debuff"]:
                self.move["debuff"][debuff] = self.move["debuff"].get(debuff, 0)
                self.move["debuff"][debuff] += move["debuff"][debuff]
        if move["buff"] != "None":
            for buff in move["buff"]:
                self.move["buff"][buff] = self.move["buff"].get(buff, 0)
                self.move["buff"][buff] += move["buff"][buff]
        if self.buff_bar["lifesteal"]:
            self.move["heal"] += self.move["damage"]
        if self.buff_bar["armor"]:
            self.move["block"] += self.buff_bar["armor"]
        return move_type

    def update(self, damage, debuff):
        if self.debuff_bar["vulnerable"]:
            damage *= 1.25
        if self.debuff_bar["marked"] and damage:
            damage += self.debuff_bar["marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        self.block = self.move["block"]
        self.health += self.move["heal"]
        self.health += self.buff_bar["regeneration"]
        if self.health > self.metadata["hp"]:
            self.health = self.metadata["hp"]
        damage += self.debuff_bar["wounded"]
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if debuff != "None":
            for effect in debuff:
                self.debuff_bar[effect] += debuff[effect]
        if self.move["buff"] != "None":
            for buff in self.move["buff"]:
                self.buff_bar[buff] += self.move["buff"][buff]


class MsG(Boss):
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.special = 0
        self.health = None
        self.status_bar = {"weakness": 0, "vulnerable": 0, "disappointment": 0, "wounded": 0, "marked": 0}
        self.buff_bar = {"power": 0, "lifesteal": 0, "regeneration": 0, "armor": 0}
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
        if self.buff_bar["lifesteal"]:
            move["heal"] += move["damage"]
        if self.buff_bar["armor"]:
            move["block"] += self.buff_bar["armor"]
        if self.status_bar["weakness"]:
            move["damage"] *= 0.75
        if self.buff_bar["power"]:
            move["damage"] *= 1.25
        self.health += move["heal"]
        self.block += move["block"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        if self.status_bar["vulnerable"]:
            damage *= 1.25
        if self.status_bar["marked"] and damage:
            damage += self.status_bar["marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.status_bar["wounded"]
        self.health += self.buff_bar["regeneration"]
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
        self.status_bar = {"weakness": 0, "vulnerable": 0, "disappointment": 0, "wounded": 0, "marked": 0}
        self.buff_bar = {"power": 0, "lifesteal": 0, "regeneration": 0, "armor": 0}
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
        if self.buff_bar["lifesteal"]:
            move["heal"] += move["damage"]
        if self.buff_bar["armor"]:
            move["block"] += self.buff_bar["armor"]
        if self.status_bar["weakness"]:
            move["damage"] *= 0.75
        if self.buff_bar["power"]:
            move["damage"] *= 1.25
        self.health += move["heal"]
        if move["buff"] != "None":
            self.buff_bar[move["buff"][0]] = move["buff"][1]
        self.block += move["block"]
        return move_type, move["phrases"][random.randint(0, len(move["phrases"]) - 1)], move["damage"], move["status"]

    def update(self, damage, status_effects):
        if self.status_bar["vulnerable"]:
            damage *= 1.25
        if self.status_bar["marked"] and damage:
            damage += self.status_bar["marked"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        damage += self.status_bar["wounded"]
        self.health += self.buff_bar["regeneration"]
        self.health -= damage
        self.damaged = False
        if damage:
            self.damaged = True
        for action in status_effects:
            if action != "None":
                for effect in action:
                    self.status_bar[effect] += action[effect]
