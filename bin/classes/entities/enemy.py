class Enemy:
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.block = 0
        self.status_bar = {"Weakness": 0, "Vulnerable": 0, "Disappointment": 0, "Pained": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Armor": 0}
        self.name = None
        self.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}, "phrase": {}}
        self.image = None
        self.phrases = None

    def initialize(self, name, phrases_data):
        self.name = name
        print(phrases_data)
        self.attacks = {a: self.metadata["attacks"][b] for a, b in enumerate(self.metadata["attacks"])}
        self.health = self.metadata["hp"]
        self.phrases = phrases_data
        self.phrases["enemy_intro"]["text"] = self.phrases["enemy_intro"]["text"].replace("---", self.metadata["name"])
        self.phrases["enemy_player_death"][0]["text"] = self.phrases["enemy_player_death"][0]["text"].replace("---", self.metadata["name"])
        self.phrases["enemy_death"]["text"] = self.phrases["enemy_death"]["text"].replace("---", self.metadata["name"])

    def act(self, turn_counter):
        attack = self.attacks[turn_counter % len(self.attacks)]
        mod = 1
        if self.status_bar["Weakness"]:
            mod *= 0.75
        if self.buff_bar["Power"]:
            mod *= 1.25
        self.attack["damage"] += attack["damage"] * mod
        self.attack["block"] += attack["block"]
        self.attack["heal"] += attack["heal"]
        if attack["status"] != "None":
            for status in attack["status"]:
                self.attack["status"][status] = self.attack["status"].get(status, 0)
                self.attack["status"][status] += attack["status"][status]
        if attack["buff"] != "None":
            for buff in attack["buff"]:
                self.attack["buff"][buff] = self.attack["buff"].get(buff, 0)
                self.attack["buff"][buff] += attack["buff"][buff]
        if self.buff_bar["Lifesteal"]:
            self.attack["heal"] += self.attack["damage"]
        self.health += attack["heal"]
        if self.buff_bar["Armor"]:
            self.attack["block"] += self.buff_bar["Armor"]
        self.block = self.attack["block"]
        self.phrases["enemy_basic"] = {"text": "{} used {}!!!".format(self.metadata["name"], attack["attack"]), "clear": True, "delay": 0.2,
                                       "fade_in": True, "fade_out": True, "line": 1, "pause": 1.0, "shake": [0, 0], "wait": 0.5}

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
        if self.attack["buff"] != "None":
            for buff in self.attack["buff"]:
                self.buff_bar[buff] += self.attack["buff"][buff]
