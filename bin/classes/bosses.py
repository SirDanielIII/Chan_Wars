import bin.blit_tools as blit

class Boss:
    def __init__(self, name, rows, columns, hp, basic, special, phrases, screen):
        self.name = name
        self.rows = rows
        self.columns = columns
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
            case "Attack":
                self.action = 0
                return self.attack_action()
            case "Quote":
                self.action = 1
                return self.talk()
            case "Die":
                self.action = 2
                return self.death()
            case "Special":
                self.action = 3
                return self.special_action()
        if "Death":
            self.run = False

    def attack_action(self):
        self.trigger = "Quote", 4
        return attack_power

    def talk(self):
        blit.draw_text(self.phrases[self.trigger[1]], self.colour, "Comic Sans MS", self.screen, (100, 100))
        return None

    def death(self):
        self.trigger = "Quote", -1
        return "Death"


class Mrs.G(Boss):
    def __init__(self):
        self.siberia = True
        self.attack_power =

