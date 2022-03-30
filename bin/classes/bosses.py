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
        match self.trigger:
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
            case "kill":
                self.action = 4
                    return self.kill()
        if "death":
            self.run = False


class DevilChan(Boss):
    def __init__(self):
        pass

    def trigger(self):
        if self.acting:
            trigger = "attack"
        if self.health <

    def special_action(self):

    def basic_action(self):

    def quote(self):


class MsG(Boss):
    def __init__(self, name, rows, columns, hp, basic, special, phrases, screen):
        super().init(name, rows, columns, hp, basic, special, phrases, screen)

    def basic_action(self):

    def trigger(self):
        if self.acting:
            trigger = "attack"
        if self.health <

    def special_action(self):

    def basic_action(self):

    def quote(self):



class MrPhone(Boss):
    def __init__(self):
        pass

    def trigger(self):

    def special_action(self):

    def basic_action(self):

    def quote(self):
