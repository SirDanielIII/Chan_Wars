import yaml  # https://zetcode.com/python/yaml/
import os


# Note: [DEVIL CHAN ONLY] The values in Special Attack goes like [Attack Type, Damage, Heal]

class Config(object):
    def __init__(self):
        # Settings
        self.player_hp = None
        self.enable_music = None
        self.enable_sfx = None
        self.music_vol = None
        self.sfx_vol = None
        self.fps_show = None
        self.fps_30 = None
        self.fps_60 = None
        self.fps_75 = None
        self.fps_165 = None
        # Data
        self.data = None
        self.default = {'bosses':
                            {'DevilChan':
                                 {'basic': ['devilish_stab', 10], 'columns': 4, 'energy': 3, 'hp': 50, 'name': 'Devil Chan',
                                  'phrases': {'attack': ['For My Lost Love!', 'World Shaking Explosion Fist!', 'North Star Spear!',
                                                         'Million Soul Bomb!', 'Burning Sun Beam!'], 'death': [
                                      'I have resigned myself. You have won. To one warrior to another, beware of the thinking question.'],
                                              'opening': ['Angel Chan... I loved you! How could you do this?!'],
                                              'special': ["That's a neat little hack.",
                                                          "With this hack, I'll steal your health for myself.",
                                                          "I hope you're prepared for this."]}, 'rows': 3,
                                  'special': ['neat_hack', 10, 10]},
                             'MrPhone': {'basic': ['disappointment', 0], 'columns': 4, 'energy': 5, 'hp': 200,
                                         'kill': ['thinking_question', 9999], 'name': 'Mr. Phone', 'phrases': {
                                     'attack': ['You need to touch grass.', 'My son could beat you at this game.',
                                                'Easy choices hard life, hard choices easy life.', "It's only awkward if you make it awkward.",
                                                'You have to build capacity.', "You chose that? Come on, that's ct!!!"],
                                     'death': ['Huh. Looks like you did practice perfectly.'],
                                     'kill': ['Next time, practice perfectly.', 'My record just increased.'],
                                     'opening': ['Did you write your TQPs?'],
                                     'special': ['Almost everything is a choice.. .including breathing!', 'Reflect, reflect, REFLECT HARDER!!!',
                                                 'Face the monster... ME!', 'Keep your head on a swivel!']}, 'rows': 7,
                                         'special': ['emotional_damage', 0]},
                             'MsG': {'basic': ['roast', 15], 'columns': 4, 'energy': 4, 'hp': 100, 'name': 'Ms. G', 'phrases': {
                                 'attack': ['For Sean!', "One of them is a woman, the other has an Indian accent if you're into it.",
                                            "I'll only give you 100% if youâ€™re one of my favourite students.", 'Do it on Repl.',
                                            "Don't ask me, use your brain."], 'death': [
                                     'Very well. you have bested me. As a warning, beware the thinking question. It will spell your doom.'],
                                 'opening': ['Sean!', "Wait, you're not Sean!"],
                                 'special': ['You! Go to Siberia!', 'You deserve to go to Siberia!']}, 'rows': 5,
                                     'special': ['siberia', 'siberia']}},
                        'player': {'hp': 50},
                        'settings': {'audio': {'enable_music': True, 'enable_sfx': True, 'music_vol': 1.0, 'sfx_vol': 1.0},
                                     'fps': {'show': False, 30: False, 60: False, 75: False, 165: True}}}
        # Add line about broomstick for Ms. G
        # Add levels beaten

    def load_config(self):
        if not os.path.exists(os.getcwd() + "/config.yml"):
            with open(os.getcwd() + "/config.yml", "w") as f:
                yaml.dump(self.default, f)
                self.default = None
        with open(os.getcwd() + "/config.yml", "r") as f:
            self.data = yaml.safe_load(f)
            self.player_hp = self.data["player"]["hp"]
            self.enable_music = self.data["settings"]["audio"]["enable_music"]
            self.enable_sfx = self.data["settings"]["audio"]["enable_sfx"]
            self.music_vol = self.data["settings"]["audio"]["music_vol"]
            self.sfx_vol = self.data["settings"]["audio"]["sfx_vol"]
            self.fps_show = self.data["settings"]["fps"]["show"]
            self.fps_30 = self.data["settings"]["fps"][30]
            self.fps_60 = self.data["settings"]["fps"][60]
            self.fps_75 = self.data["settings"]["fps"][75]
            self.fps_165 = self.data["settings"]["fps"][165]

    def get_config(self):
        # print(self.player_hp, self.enable_music, self.enable_sfx, self.music_vol, self.sfx_vol,
        #       self.fps_show, self.fps_30, self.fps_60, self.fps_75, self.fps_165)
        return self.data

    def get_boss_dict(self, name):
        return self.data.get("bosses").get(name)

    def get_boss_stat(self, boss, header):
        # name: str | energy: int | rows: int | columns: int | hp: int
        # basic: list | special: list | kill: list | phrases: dictionary
        # List for basic, special and kill are one element describing the act and another describing the effect of the action
        return self.data.get("bosses").get(boss).get(header)

    def get_player_dict(self, name):
        return self.data.get("player").get(name)

    def get_player_stat(self, key, header):
        return self.data.get("player").get(key).get(header)

    def get_settings_dict(self, name):
        return self.data.get("settings").get(name)

    def get_settings_stat(self, key, header):
        return self.data.get("settings").get(key).get(header)

# # Test
# yeet = Config()
# yeet.load_config()
# print(yeet.get_config())
# print(yeet.get_boss_info("mr_phone"))
# print(yeet.get_boss_stat("mr_phone", "hp"))
