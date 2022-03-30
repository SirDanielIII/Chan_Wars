# https://zetcode.com/python/yaml/

import yaml
import os


class Config(object):
    def __init__(self):
        self.data = None
        self.default = {'player': {'hp': 50},
                        'bosses': {'devil_chan':
                                       {'name': 'Devil Chan',
                                        'energy': 3,
                                        'rows': 3,
                                        'columns': 4,
                                        'hp': 50,
                                        'basic': ['devilish_stab', 10],
                                        'special': ['neat_hack', 10, 10],
                                        'phrases':
                                            {'opening': ['Angel Chan... I loved you! How could you do this?!'],
                                             'attack': ['For My Lost Love!', 'World Shaking Explosion Fist!', 'North Star Spear!',
                                                        'Million Soul Bomb!', 'Burning Sun Beam!'],
                                             'special': ["That's a neat little hack.", "With this hack, I'll steal your health for myself.",
                                                         "I hope you're prepared for this."],
                                             'death': ['Ihave resigned myself. '
                                                       'You have won. To one warrior to another, beware of the thinking question.']}},
                                   'ms_g': {'name': 'Ms. G',
                                            'energy': 4,
                                            'rows': 5,
                                            'columns': 4,
                                            'hp': 100,
                                            'basic': ['roast', 15],
                                            'special': ['siberia', 'siberia'],
                                            'phrases':
                                                {'opening': ['Sean!', "Wait, you're not Sean!"],
                                                 'attack': ['For Sean!', "One of them is a woman, the other has an Indian accent if you're into it.",
                                                            "I'll only give you 100% if youâ€™re one of my favourite students.",
                                                            'Do it on Repl.', "Don't ask me, use your brain."],
                                                 'special': ['You! Go to Siberia!', 'You deserve to go to Siberia!'],
                                                 'death': ['Very well. you have bested me. As a warning, beware the thinking question. '
                                                           'It will spell your doom.']}},
                                   'mr_phone': {'name': 'Mr. Phone',
                                                'energy': 5,
                                                'rows': 7,
                                                'columns': 4,
                                                'hp': 200,
                                                'basic': ['disappointment', 0],
                                                'special': ['emotional_damage', 0],
                                                'kill': ['thinking_question', 9999],
                                                'phrases': {'opening': ['Did you write your TQPs?'],
                                                            'attack': ['You need to touch grass.',
                                                                       'My son could beat you at this game.',
                                                                       'Easy choices hard life, hard choices easy life.',
                                                                       "It's only awkward if you make it awkward.",
                                                                       'You have to build capacity.',
                                                                       "You chose that? Come on, that's ct!!!"],
                                                            'special': ['Almost everything is a choice.. .including breathing!',
                                                                        'Reflect, reflect, REFLECT HARDER!!!',
                                                                        'Face the monster... ME!',
                                                                        'Keep your head on a swivel!'],
                                                            'kill': ['Next time, practice perfectly.',
                                                                     'My record just increased.'],
                                                            'death': ['Huh. Looks like you did practice perfectly.']}}},
                        'settings': {
                            'fps': {'show': False,
                                    30: False,
                                    60: False,
                                    75: False,
                                    165: True},
                            'audio': {
                                'enable_sfx': True,
                                'enable_music': True,
                                'sfx_vol': 1.0,
                                'music_vol': 1.0}}}
        # Add line about broomstick for Ms. G
        # Note: The values in Special Attack goes like [Attack Type, Damage, Heal]
        #       This ONLY goes for Devil Chan

    def load_config(self):
        if not os.path.exists(os.getcwd() + "/config.yml"):
            print("[CW] Config file does not exist! Generating a new one :D")
            with open(os.getcwd() + "/config.yml", "w") as f:
                yaml.dump(self.default, f)
                self.default = None
        with open(os.getcwd() + "/config.yml", "r") as f:
            self.data = yaml.safe_load(f)

    def get_config(self):
        return self.data

    def get_boss_dict(self, name):
        return self.data.get("bosses").get(name)

    def get_boss_stat(self, boss, header):
        # name: str | energy: int | rows: int | columns: int | hp: int
        # basic: str | special: str | kill: str | phrases: []
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
