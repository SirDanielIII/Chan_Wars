import random



class Boss:
    def __init__(self, surface, configuration):
        self.data = None
        self.screen = surface
        self.trigger = None
        self.alive = True
        self.config = configuration

    def act(self):
        match self.trigger:
            case "attack":
                return basic, self.basic_action()
            case "die":
                return death, self.death()
            case "special":
                return special, self.special_action()
            case "kill":
                return kill, self.kill()
        if "death":
            self.alive = False

    def basic_action(self):
        return self.basic_power, self.attack_phrases[random.randint(0, len(self.attack_phrases) - 1)]


class DevilChan(Boss):
    def __init__(self, surface, configuration):
        super().init(surface, configuration)
        self.data = self.config["DevilChan"]
        self.special = 0
        self.health = self.data["hp"]
        self.energy = self.data["energy"]
        self.basic_power = self.data["basic"][1]
        self.attack_phrases = self.data["phrases"]["basic"]

    def update(self, damage):
        self.health -= damage
        self.energy = self.data["energy"]
        return self.health, self.energy

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if self.health < self.data["hp"] // 2 and not self.special:
                self.trigger = "special"
            if self.health <= 0:
                self.trigger = "die"

    def special_action(self):
        self.health += self.data["special"][2]
        self.special = 1
        return self.data["special"][1], self.data["phrases"]["special"][random.randint(0, len(self.data["phrases"]["special"]) - 1)], self.health

    def death(self):
        self.alive = False
        return self.data["phrases"]["death"]


class MsG(Boss):
    def __init__(self, surface, configuration):
        super().init(surface, configuration)
        self.data = self.config["MsG"]
        self.special = 0
        self.health = self.data["hp"]
        self.energy = self.data["energy"]
        self.siberia = False
        self.basic_power = self.data["basic"][1]
        self.attack_phrases = self.data["phrases"]["basic"]

    def update(self, damage):
        self.health -= damage
        if self.siberia:
            self.energy = self.data["energy"] - 1
        else:
            self.energy = self.data["energy"]
        return self.health, self.energy, self.siberia

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if self.health != self.data["hp"] and self.health > self.data["hp"] // 2:
                self.special = 0
            if (self.health == self.data["hp"] and not self.special) or (self.health <= self.data["hp"] // 2 and not self.special):
                self.trigger = "special"
            if self.health <= 0:
                self.trigger = "die"

    def special_action(self):
        if self.health > self.data["hp"] // 2:
            self.special = 1
            self.siberia = self.data["special"][1]
            return self.siberia, self.data["phrases"]["special"][random.randint(0, len(self.data["phrases"]["special"]) - 1)]
        else:
            self.special = 1
            self.siberia = False
            return self.siberia, self.data["phrases"]["special"]["out"]

    def death(self):
        return self.data["phrases"]["death"]


class MrPhone(Boss):
    def __init__(self, surface, configuration):
        super().init(surface, configuration)
        self.data = self.config["MrPhone"]
        self.special = 0
        self.health = self.data["hp"]
        self.energy = self.data["energy"]
        self.basic_power = self.data["basic"][1]
        self.attack_phrases = self.data["phrases"]["basic"]
        self.damaged = True
        self.turn_count = 1

    def update(self, damage, turn_counter):
        self.health -= damage
        self.damaged = False
        if damage:
            self.damaged = True
        self.turn_count = turn_counter
        self.energy = self.data["energy"]
        return self.health, self.energy

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if not self.turn_count % 4:
                self.trigger = "special"
            if not self.damaged:
                self.trigger = "kill"
            if self.health <= 0:
                self.trigger = "die"

    def special_action(self):
        return self.data["phrases"]["special"][random.randint(0, len(self.data["phrases"]["special"]) - 1)]

    def kill(self):
        return self.data["kill"]["1"], self.data["phrases"]["kill"][random.randint(0, len(self.data["phrases"]["kill"]) - 1)]

    def death(self):
        return self.data["phrases"]["death"]
