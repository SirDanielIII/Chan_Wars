class Enemy:
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.block = 0
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0, "Marked": 0}
        self.buff_bar = {"Power": 0, "Lifesteal": 0, "Regeneration": 0, "Energized": 0, "Armor": 0, "Clairvoyant": 0}
        self.name = None
        self.image = None

    def initialize(self, name):
        self.name = name
        self.attacks = {a: self.metadata["attacks"][b] for a, b in enumerate(self.metadata["attacks"])}
        self.health = self.metadata["hp"]

    def act(self, turn_counter):
        attack = self.attacks[turn_counter % len(self.attacks)]
        if self.buff_bar["Lifesteal"]:
            attack["heal"] += attack["damage"]
        self.health += attack["heal"]
        if self.buff_bar["Armor"]:
            attack["block"] += self.buff_bar["Armor"]
        self.block = attack["block"]
        if attack["buff"] != "None":
            self.buff_bar[attack["buff"][0]] += attack["buff"][1]
        phrase = "{} used {}".format(self.metadata["name"], attack["phrase"])
        if self.status_bar["Weakness"]:
            attack["damage"] *= 0.75
        if self.buff_bar["Power"]:
            attack["damage"] *= 1.25
        return "basic", phrase, attack["damage"], attack["status"]

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
        damage += self.status_bar["Poison"]
        self.health += self.buff_bar["Regeneration"]
        self.health -= damage
        print(status_effects)
        for action in status_effects:
            if action != "None":
                for effect in action:
                    self.status_bar[effect] += action[effect]
