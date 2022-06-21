class Enemy:
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.block = 0
        self.debuff_bar = {"weakness": 0, "vulnerable": 0, "disappointment": 0, "wounded": 0, "marked": 0}
        self.buff_bar = {"power": 0, "lifesteal": 0, "regeneration": 0, "armor": 0}
        self.name = None
        self.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}, "phrase": {}}
        self.image = None
        self.phrases = {}

    def initialize(self, name, phrases_data):
        self.name = name
        self.attacks = {a: self.metadata["attacks"][b] for a, b in enumerate(self.metadata["attacks"])}
        self.health = self.metadata["hp"]
        self.phrases["enemy_intro"] = {a: phrases_data["enemy_intro"][a] for a in ("text", "clear", "delay", "fade_in", "fade_out", "line", "pause", "shake", "wait")}
        self.phrases["enemy_player_death"] = {0: {a: phrases_data["enemy_player_death"][0][a] for a in ("text", "clear", "delay", "fade_in", "fade_out", "line", "pause", "shake", "wait")},
                                              1: {a: phrases_data["enemy_player_death"][1][a] for a in ("text", "clear", "delay", "fade_in", "fade_out", "line", "pause", "shake", "wait")}}
        self.phrases["enemy_death"] = {a: phrases_data["enemy_death"][a] for a in ("text", "clear", "delay", "fade_in", "fade_out", "line", "pause", "shake", "wait")}
        self.phrases["enemy_intro"]["text"] = self.phrases["enemy_intro"]["text"].replace("---", self.metadata["name"])
        self.phrases["enemy_player_death"][0]["text"] = self.phrases["enemy_player_death"][0]["text"].replace("---", self.metadata["name"])
        self.phrases["enemy_death"]["text"] = self.phrases["enemy_death"]["text"].replace("---", self.metadata["name"])

    def act(self, turn_counter):
        attack = self.attacks[turn_counter % len(self.attacks)]
        mod = 1
        if self.debuff_bar["weakness"]:
            mod *= 0.75
        if self.buff_bar["power"]:
            mod *= 1.25
        self.attack["damage"] += attack["damage"] * mod
        self.attack["block"] += attack["block"]
        self.attack["heal"] += attack["heal"]
        if attack["debuff"] != "None":
            for debuff in attack["debuff"]:
                self.attack["debuff"][debuff] = self.attack["debuff"].get(debuff, 0)
                self.attack["debuff"][debuff] += attack["debuff"][debuff]
        if attack["buff"] != "None":
            for buff in attack["buff"]:
                self.attack["buff"][buff] = self.attack["buff"].get(buff, 0)
                self.attack["buff"][buff] += attack["buff"][buff]
        if self.buff_bar["lifesteal"]:
            self.attack["heal"] += self.attack["damage"]
        if self.buff_bar["armor"]:
            self.attack["block"] += self.buff_bar["armor"]
        self.health += self.attack["heal"]
        self.phrases["enemy_basic"] = {"text": "{} used {}!!!".format(self.metadata["name"], attack["attack"]), "clear": True, "delay": 0.07,
                                       "fade_in": True, "fade_out": True, "line": 1, "pause": 1.0, "shake": [5, 5], "wait": 0.1}
        print(self.attack["heal"], 2)

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
        self.block = self.attack["block"]
        damage += self.debuff_bar["wounded"]
        self.health += self.buff_bar["regeneration"]
        if self.health > self.metadata["hp"]:
            self.health = self.metadata["hp"]
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if debuff != "None":
            for effect in debuff:
                self.debuff_bar[effect] += debuff[effect]
        if self.attack["buff"] != "None":
            for buff in self.attack["buff"]:
                self.buff_bar[buff] += self.attack["buff"][buff]
