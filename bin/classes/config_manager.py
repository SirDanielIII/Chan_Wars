# https://zetcode.com/python/yaml/

import yaml
import os


class Config(object):
    def __init__(self):
        self.data = None
        self.default = {'player': {'hp': 50}, 'bosses': {'devil_chan': {'name': 'Devil Chan', 'energy': 3, 'rows': 3, 'columns': 4,
                                                                        'hp': 50, 'basic': 'devilish_stab', 'special': 'neat_hack',
                                                                        'phrases': ["Here's a neat little hack."]},
                                                         'ms_g': {'name': 'Ms. G', 'energy': 4, 'rows': 5, 'columns': 4, 'hp': 100, 'basic': 'roast',
                                                                  'special': 'siberia',
                                                                  'phrases': ['Sean!',
                                                                              "One of them is a woman, the other has an Indian accent if you're into it.",
                                                                              "I'll only give you 100% if youâ€™re one of my favourite students.",
                                                                              'Do it on Repl.', 'Go to Siberia!',
                                                                              "Don't ask me, use your brain.", 'Troubleshoot it.', 'Gosh.']},
                                                         'mr_phone': {'name': 'Mr. Phone', 'energy': 5, 'rows': 7,
                                                                      'columns': 4, 'hp': 200, 'basic': 'disappointment',
                                                                      'special': 'emotional_damage', 'kill': 'thinking_question',
                                                                      'phrases': ['You need to touch grass.', 'My son could beat you at this game.',
                                                                                  'Easy choices hard life, hard choices easy life.',
                                                                                  "It's only awkward if you make it awkward.",
                                                                                  'Almost everything is a choice.. .including breathing!',
                                                                                  'Reflect, reflect, REFLECT HARDER!!!',
                                                                                  'Face the monster... ME!', 'Keep your head on a swivel!',
                                                                                  'You have to build capacity.', 'Practice perfectly.',
                                                                                  'My record just increased.', 'Did you write your TQPs?',
                                                                                  "You chose that? Come on, that's such a crazy talk!!!"]}},
                        'settings': {'fps': {'show': False, 30: False, 60: False, 75: False, 165: True}, 'audio': {'enable_sfx': True,
                                                                                                                   'enable_music': True,
                                                                                                                   'sfx_vol': 1.0, 'music_vol': 1.0}}}

    def load_config(self):
        if not os.path.exists(os.getcwd() + "config.yml"):
            print("[CW] Config file does not exist, generating a new one")
            with open(os.getcwd() + "/config.yml", "w") as f:
                f.dump(self.default, f)
                self.default = None
            print

        with open(os.getcwd() + "/config.yml", "r") as f:
            self.data = yaml.safe_load(f)

    def get_config(self):
        return self.data

    def get_boss_info(self, name):
        return self.data.get("bosses").get(name)

    def get_boss_stat(self, boss, header):
        # name: str | energy: int | rows: int | columns: int | hp: int
        # basic: str | special: str | kill: str | phrases: []
        return self.data.get("bosses").get(boss).get(header)

# # Test
# yeet = Config()
# yeet.load_config()
# print(yeet.get_config())
# print(yeet.get_boss_info("mr_phone"))
# print(yeet.get_boss_stat("mr_phone", "hp"))
