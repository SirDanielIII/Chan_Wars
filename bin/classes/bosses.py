import bin.blit_tools as blit
from abc import ABC, abstractmethod


class Boss:
    def __init__(self, name, rows, columns, hp, basic, special, phrases, screen):
        self.name = name
        self.hp = hp
        self.basic = basic
        self.special = special
        self.phrases = phrases
        self.color = None
        self.trigger = None
        self.screen = screen
        self.run = True

    def act(self):
        match self.trigger[0]:
            case "attack":
                self.action = 0
                return self.attack_action()
            case "quote":
                self.action = 1
                return self.talk()
            case "die":
                self.action = 2
                return self.death()
            case "special":
                self.action = 3
                return self.special_action()
        if "death":
            self.run = False

    @abstractmethod
    def trigger(self):
        pass

    @abstractmethod
    def basic_action(self):
        pass

    @abstractmethod
    def special_action(self):
        pass

    @abstractmethod
    def quote(self):
        pass


class Ms_G(Boss):
    def __init__(self):
        self.siberia = True
        self.attack_power =

    def attack_action(self):
        self.attack
