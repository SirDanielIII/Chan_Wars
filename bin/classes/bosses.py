import bin.blit_tools as blit
from abc import ABC, abstractmethod
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

    def basic_action(self, attack_power, attack_phrases):
        return attack_power, attack_phrases[random.randint(0, len(attack_phrases) - 1)]


class DevilChan(Boss):
    def __init__(self, surface, configuration):
        super().init(surface, configuration)
        self.data = configuration # pulled from config file
        self.special = 0
        self.health = max_hp # pulled from config file
        self.energy = energy # pulled from config file

    def update(self, damage):
        self.health -= damage
        self.energy = energy # pulls this value from the config file
        return self.health, self.energy

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if self.health < max_hp//2 and not self.special:
                self.trigger = "special"
            if self.health <= 0:
                self.trigger = "die"
        # max hp pulled from config file

    def special_action(self):
        self.health += healing # pulled from config file
        self.special = 1
        return attack_power, special_phrases[random.randint(0, len(special_phrases) - 1)], self.health
        # attack power and special attack pulled from config file

    def death(self):
        self.alive = False
        return death_phrase # pulled from config file


class MsG(Boss):
    def __init__(self, surface, configuration):
        super().init(surface, configuration)
        self.special = 0
        self.health = max_hp # pulled from config file
        self.energy = energy # pulled from config file
        self.siberia = False

    def update(self, damage):
        self.health -= damage
        if self.siberia:
            self.energy = energy - 1 # pulled from config file
        else:
            self.energy = energy # pulled from config file
        return self.health, self.energy, self.siberia

    def trigger(self):
        if self.acting:
            self.trigger = "attack"
            if self.health != max_hp and self.health > max_hp//2:
                self.special = 0
            if (self.health == max_hp and not self.special) or (self.health <= max_hp//2 and not self.special):
                self.trigger = "special"
            if self.health <= 0:
                self.trigger = "die"
        # max hp pulled from config file

    def special_action(self):
        if self.health > max_hp//2:
            self.special = 1
            self.siberia = True
            return self.siberia, special_phrases[random.randint(0, len(special_phrases) - 1)]
        else:
            self.special = 1
            self.siberia = False
            return self.siberia, out_of_siberia
        # max_hp, special_phrases, out_of_siberia pulled from config file

    def death(self):
        return death_phrase # pulled from config file


class MrPhone(Boss):
    def __init__(self, surface, configuration, energy, max_hp):
        super().init(surface, configuration)
        self.special = 0
        self.health = max_hp # pulled from config file
        self.energy = energy # pulled from config file
        self.damaged = True
        self.turn_count = 1

    def update(self, damage, turn_counter):
        self.health -= damage
        self.damaged = False
        if damage:
            self.damaged = True
        self.turn_count = turn_counter
        self.energy = energy # pulls this value from the config file
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
        # max hp pulled from config file

    def special_action(self):
        return special_phrases[random.randint(0, len(special_phrases) - 1)]
        # special attack pulled from config file

    def kill(self):
        return attack_power, kill_phrase[random.randint(0, len(kill_phrases) - 1)]
        # attack power and kill attack pulled from config file

    def death(self):
        return death_phrase # pulled from config file