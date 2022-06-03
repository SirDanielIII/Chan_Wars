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
        self.trigger = None
        self.special = 0
        self.health = None
        self.energy = None
        self.basic_power = None
        self.attack_phrases = None
        self.special = 0
        self.damaged = True
        self.turn_count = 0

    def load_boss_info(self):
        self.health = self.metadata["boss"]["hp"]
        self.energy = self.metadata["player"]["energy"]
        self.basic_power = self.metadata["boss"]["basic"][1]
        self.attack_phrases = self.metadata["boss"]["phrases"]["attack"]

    def update(self, damage, turn_counter=0):
        self.health -= damage
        self.damaged = False
        if damage:
            self.damaged = True
        self.turn_count = turn_counter
        self.energy = self.metadata["player"]["energy"]
        return self.health, self.energy

    def trigger_method(self):
        self.trigger = "attack"
        if not self.turn_count % 4:
            self.trigger = "special"
        if not self.damaged:
            self.trigger = "kill"
        if self.health <= 0:
            self.trigger = "die"

    def act(self):
        match self.trigger:
            case "attack":
                return self.trigger, self.basic_action()
            case "die":
                return self.trigger, self.death()
            case "special":
                return self.trigger, self.special_action()
            case "kill":
                return self.trigger, self.kill()

    def kill(self):
        return self.metadata["boss"]["kill"][1], self.metadata["boss"]["phrases"]["kill"][random.randint(0, len(self.metadata["boss"]["phrases"]["kill"]) - 1)], "good_game"

    def death(self):
        return self.metadata["boss"]["phrases"]["death"], "death"

    def basic_action(self):
        return self.basic_power, self.attack_phrases[random.randint(0, len(self.attack_phrases) - 1)], "thinking_question"

    def special_action(self):
        return self.metadata["boss"]["special"][1], self.metadata["boss"]["phrases"]["special"][random.randint(0, len(self.metadata["boss"]["phrases"]["special"]) - 1)], "disappointment"
