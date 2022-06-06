class Enemy:
    def __init__(self, config):
        super().__init__()
        self.metadata = config
        self.health = None
        self.energy = None
        self.attacks = None
        self.block = 0
        self.status_bar = {"Fear": 0, "Weakness": 0, "Blindness": 0, "Vulnerable": 0, "Disappointment": 0, "Poison": 0}
        self.buff_bar = {"Power": 0, "Regeneration": 0, "Dodge": 0, "Armor": 0, "Clairvoyant": 0}
        self.name = None
        self.image = None

    def initialize_type(self, name):
        self.name = name
        self.attacks = {a: self.metadata["enemies"][self.name]["attacks"][b] for a, b in enumerate(self.metadata["enemies"][self.name]["attacks"])}
        self.energy = self.metadata["player"]["energy"]
        self.health = self.metadata["enemies"][self.name]["hp"]

    def act(self, turn_counter):
        attack = self.attacks[turn_counter % len(self.attacks)]
        self.health += attack["heal"]
        self.block = attack["block"]
        if attack["buff"] != "None":
            self.buff_bar[attack["buff"][0]] += attack["buff"][1]
        phrase = "{} used {}".format(self.metadata["enemies"][self.name]["name"], attack["phrase"])
        return "basic", phrase, attack["damage"], attack["status"]

    def update(self, damage, status_effects):
        self.energy = self.metadata["player"]["energy"]
        if self.block >= damage:
            damage = 0
        else:
            damage -= self.block
        self.block = 0
        self.health -= damage
        if status_effects != "None":
            self.status_bar[status_effects[0]] += status_effects[1]
