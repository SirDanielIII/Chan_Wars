import yaml  # https://zetcode.com/python/yaml/
import os
import pygame as pg


# Note: [DEVIL CHAN ONLY] The values in Special Attack goes like [Attack Type, Damage, Heal]

class Config(object):
    def __init__(self):
        # Images
        self.menu_img = None
        self.boss_card = None
        self.end_screens = None
        self.image_dict = None
        self.face_images = None
        self.backgrounds = None
        self.enemies_images = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Fonts
        self.f_hp_bar_hp = None
        self.f_hp_bar_name = None
        self.f_boss_text = None
        self.f_options_title = None
        self.f_options_sub = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Other
        self.highest_level_beat = None
        self.boss_face_size = None
        self.chan_card_size = None
        self.boss_face_size = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Settings
        self.enable_music = None
        self.enable_sfx = None
        self.music_vol = None
        self.sfx_vol = None
        self.fps_show = None
        self.fps_value = 165  # Needs to have a value set due to boot menu
        self.levels = None
        self.bosses = None
        # Config File Data
        self.global_conf = None
        self.level_confs = None
        self.boss_confs = None

    def load_global_conf(self):
        if not os.path.exists(os.getcwd() + "/configuration/config.yml"):
            with open(os.getcwd() + "/configuration/config.yml", "w") as f:
                yaml.dump(
                    {'settings': {'audio': {'enable_music': True, 'enable_sfx': True, 'music_vol': 1.0, 'sfx_vol': 1.0},
                                  'fps': {'show': False, 'value': 165}, 'fullscreen': False},
                     'other': {'levels': 3, 'bosses': ['devil_chan', 'mr_phone', 'ms_g'], 'boss_face_size': {'x': 500, 'y': 500},
                               'highest_level_beat': 0}}
                    , f)  # Create config file with default values if it doesn't exist

        with open(os.getcwd() + "/configuration/config.yml", "r") as f:
            self.global_conf = yaml.safe_load(f)  # Save .yml file into variable
            self.enable_music = self.global_conf["settings"]["audio"]["enable_music"]
            self.enable_sfx = self.global_conf["settings"]["audio"]["enable_sfx"]
            self.music_vol = self.global_conf["settings"]["audio"]["music_vol"]
            self.sfx_vol = self.global_conf["settings"]["audio"]["sfx_vol"]
            self.fps_show = self.global_conf["settings"]["fps"]["show"]
            self.fps_value = self.global_conf["settings"]["fps"]["value"]
            self.levels = self.global_conf["other"]["levels"]
            self.bosses = self.global_conf["other"]["bosses"]
            self.highest_level_beat = self.global_conf["other"]["highest_level_beat"]
            self.boss_face_size = self.global_conf["other"]["boss_face_size"]

    def load_level_confs(self):  # Run this after load_global_config()
        self.level_confs = {}
        for i in range(self.levels):
            filename = "level_" + str(i)
            if not os.path.exists(os.getcwd() + "/configuration/levels/" + filename + ".yml"):
                with open(os.getcwd() + "/configuration/levels/" + filename + ".yml", "w") as f:
                    match i:
                        case 1:
                            self.level_confs[i] = {
                                'level_1':
                                    {'player': {'hp': 50, 'columns': 3, 'energy': 3, 'rows': 4,
                                                'cards': {'air_chan': {'block': 5, 'buff': 'None', 'heal': 5, 'status': ['Weakness', 2], 'damage': 0},
                                                          'angel_chan': {'block': 0, 'buff': 'None', 'heal': 10, 'status': 'None', 'damage': 5},
                                                          'avatar_chan': {'block': 5, 'buff': ['Power', 1], 'heal': 5, 'status': ['Weakness', 1], 'damage': 5},
                                                          'earth_chan': {'block': 10, 'buff': ['Armor', 3], 'heal': 0, 'status': 'None', 'damage': 0},
                                                          'farquaad_chan': {'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Marked', 3], 'damage': 10},
                                                          'fire_chan': {'block': 0, 'buff': ['Power', 2], 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'jackie_chan': {'block': 10, 'buff': ['Energized', 1], 'heal': 0, 'status': ['Weakness', 2], 'damage': 0},
                                                          'jesus_chan': {'block': 0, 'buff': ['Clairvoyant', 2], 'heal': 15, 'status': 'None', 'damage': 0},
                                                          'oni_chan': {'block': 0, 'buff': ['Power', 2], 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'shrek_chan': {'block': 10, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'square_chan': {'block': 0, 'buff': ['Clairvoyant', 2], 'heal': 0, 'status': ['Marked', 3], 'damage': 0},
                                                          'un-chany_chan': {'block': 0, 'buff': ['Energized', 1], 'heal': 0, 'status': 'None', 'damage': 15},
                                                          'upsidedown_chan': {'block': 10, 'buff': ['Lifesteal', 2], 'heal': 0, 'status': 'None', 'damage': 5},
                                                          'water_chan': {'block': 0, 'buff': ['Regeneration', 5], 'heal': 10, 'status': 'None', 'damage': 0}}}},
                                'boss': {
                                    'moves': {'basic_1': {'phrases': ['For My Lost Love!', 'World Shaking Explosion Fist!', 'North Star Spear!'], 'damage': 15,
                                                          'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0},
                                              'basic_2': {'phrases': ['Million Soul Bomb!', 'Burning Sun Beam!', 'Point Two Electron Volts!'], 'damage': 10,
                                                          'block': 0, 'status': ['Weakness', 2], 'buff': ['Armor', 10], 'heal': 0},
                                              'basic_3': {'phrases': ['Face my wrath!', 'Prepare yourself for the ultimate doom!', 'You are not prepared!'],
                                                          'damage': 0, 'block': 15, 'buff': ['Power', 1], 'status': ['Vulnerable', 1], 'heal': 0},
                                              'special': {'phrases': ["That's a neat little hack that I found!", "With this hack, I'll steal your health for myself.",
                                                                      "I hope you're prepared for this.", "You know, I'm something of a scientist myself."],
                                                          'damage': 10, 'block': 0, 'status': 'None', 'buff': ['Lifesteal', 2], 'heal': 20},
                                              'death': {'phrases': ['NOOOOOOO!!!', 'THIS IS BLASPHEMYYYYYY!!! *dies*'], 'damage': 0, 'block': 0,
                                                        'status': 'None', 'buff': 'None', 'heal': 0}},
                                    'hp': 60, 'name': 'Devil Chan', 'phrases': {'intro': [['Angel Chan...', 0.1, [0, 0], 1.0],
                                                                                          ['I loved you!', 0.3, [5, 0]],
                                                                                          ['How could you do this!?', 0.2, [20, 20]]]}},
                                'enemies':
                                    {'flying': {'hp': 50, 'name': 'Flying Chan',
                                                'attacks': {'swoop_in': {'phrase': 'Swoop In', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Fear', 1]},
                                                            'claw_strike': {'phrase': 'Claw Strike', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                            'fly_Up': {'phrase': 'Fly Up', 'damage': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'block': 10}}},
                                     'drowned': {'hp': 30, 'name': 'Drowned Chan',
                                                 'attacks': {
                                                     'drowned_glare': {'phrase': 'Drowned Glare', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Fear', 1]},
                                                     'bloated_breath': {'phrase': 'Bloated Breath', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0,
                                                                        'status': ['Vulnerable', 1]},
                                                     'corpse_explosion': {'phrase': 'Corpse Explosion', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': -30, 'damage': 25}}},
                                     'big': {'hp': 75, 'name': 'Big Chan',
                                             'attacks': {'big_smack': {'phrase': 'Biggus Smackus', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 15}}},
                                     'dark': {'hp': 40, 'name': 'Dark Chan',
                                              'attacks': {'dark_orb': {'phrase': 'Dark Orb', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0, 'damage': 10},
                                                          'darkness': {'phrase': 'Darkness', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Weakness', 2]},
                                                          'curse': {'phrase': 'Dark Curse', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Vulnerable', 1]}}},
                                     'goblin': {'hp': 30, 'name': 'Goblin Chan',
                                                'attacks': {
                                                    'evasive_maneuvers': {'phrase': 'Evasive Maneuvers', 'damage': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'block': 10},
                                                    'tiny_stab': {'phrase': 'Tiny Stab', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                    'hamstring': {'phrase': 'Hamstring', 'damage': 0, 'buff': 'None', 'heal': 0, 'block': 0, 'status': ['Weakness', 2]}}},
                                     'bat': {'hp': 40, 'name': 'Bat Chan',
                                             'attacks': {'sonic_attack': {'phrase': 'Sonic Attack', 'block': 0, 'status': 'None', 'damage': 10, 'buff': 'None', 'heal': 0},
                                                         'resonate': {'phrase': 'Resonate', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Weakness', 1]}}}}}
                        case 2:
                            self.level_confs[i] = {
                                'level_2':
                                    {'player': {'hp': 75, 'columns': 5, 'energy': 4, 'rows': 4,
                                                'cards': {'air_chan': {'block': 5, 'buff': 'None', 'heal': 5, 'status': ['Weakness', 2], 'damage': 0},
                                                          'angel_chan': {'block': 0, 'buff': 'None', 'heal': 10, 'status': 'None', 'damage': 5},
                                                          'avatar_chan': {'block': 5, 'buff': ['Power', 1], 'heal': 5, 'status': ['Weakness', 1], 'damage': 5},
                                                          'earth_chan': {'block': 10, 'buff': ['Armor', 3], 'heal': 0, 'status': 'None', 'damage': 0},
                                                          'farquaad_chan': {'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Marked', 3], 'damage': 10},
                                                          'fire_chan': {'block': 0, 'buff': ['Power', 2], 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'jackie_chan': {'block': 10, 'buff': ['Energized', 1], 'heal': 0, 'status': ['Weakness', 2], 'damage': 0},
                                                          'jesus_chan': {'block': 0, 'buff': ['Clairvoyant', 2], 'heal': 15, 'status': 'None', 'damage': 0},
                                                          'oni_chan': {'block': 0, 'buff': ['Power', 2], 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'shrek_chan': {'block': 10, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'square_chan': {'block': 0, 'buff': ['Clairvoyant', 2], 'heal': 0, 'status': ['Marked', 3], 'damage': 0},
                                                          'un-chany_chan': {'block': 0, 'buff': ['Energized', 1], 'heal': 0, 'status': 'None', 'damage': 15},
                                                          'upsidedown_chan': {'block': 10, 'buff': ['Lifesteal', 2], 'heal': 0, 'status': 'None', 'damage': 5},
                                                          'water_chan': {'block': 0, 'buff': ['Regeneration', 5], 'heal': 10, 'status': 'None', 'damage': 0}}}},
                                'boss': {
                                    'moves': {'basic_1': {'phrases': ['For Sean!', "I'll only give you 100% if youâ€™re one of my favourite students."],
                                                          'damage': 15, 'block': 0, 'status': ['Vulnerable', 1], 'buff': 'None', 'heal': 0},
                                              'basic_2': {'phrases': ["Don't ask me, use your brain.", 'I have WELHpon *pulls out a meter stick*'],
                                                          'damage': 15, 'block': 0, 'status': ['Weakness', 2], 'buff': 'None', 'heal': 0},
                                              'special': {'phrases': ['You! Go to Siberia!', 'You deserve to go to Siberia!'],
                                                          'damage': 0, 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0},
                                              'death': {'phrases': ['why must you use... list comphrehension... *dies*'],
                                                        'damage': 0, 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0},
                                              'siberia': {'phrases': ['You!!! How did you escape Siberia!?'], 'damage': 0, 'block': 0, 'status': 'None',
                                                          'buff': 'None', 'heal': 0},
                                              'hp': 100, 'name': 'Ms. G', 'phrases': {'intro': ['Hello Sean!', 'How are you doing?', "Wait, you're not Sean!"]}}},
                                'enemies':
                                    {'flying': {'hp': 75, 'name': 'Flying Chan',
                                                'attacks': {'swoop_in': {'phrase': 'Swoop In', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Fear', 2]},
                                                            'claw_strike': {'phrase': 'Claw Strike', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 15},
                                                            'fly_Up': {'phrase': 'Fly Up', 'damage': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'block': 20}}},
                                     'drowned': {'hp': 40, 'name': 'Drowned Chan',
                                                 'attacks': {
                                                     'drowned_glare': {'phrase': 'Drowned Glare', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Fear', 2]},
                                                     'bloated_breath': {'phrase': 'Bloated Breath', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0,
                                                                        'status': ['Vulnerable', 1]},
                                                     'corpse_explosion': {'phrase': 'Corpse Explosion', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': -40, 'damage': 35}}},
                                     'big': {'hp': 100, 'name': 'Big Chan',
                                             'attacks': {'big_smack': {'phrase': 'Biggus Smackus', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 15}}},
                                     'dark': {'hp': 50, 'name': 'Dark Chan',
                                              'attacks': {'dark_orb': {'phrase': 'Dark Orb', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0, 'damage': 20},
                                                          'darkness': {'phrase': 'Darkness', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Weakness', 2]},
                                                          'curse': {'phrase': 'Dark Curse', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Vulnerable', 1]}}},
                                     'goblin': {'hp': 35, 'name': 'Goblin Chan',
                                                'attacks': {
                                                    'evasive_maneuvers': {'phrase': 'Evasive Maneuvers', 'damage': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'block': 20},
                                                    'tiny_stab': {'phrase': 'Tiny Stab', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                    'hamstring': {'phrase': 'Hamstring', 'damage': 0, 'buff': 'None', 'heal': 0, 'block': 0, 'status': ['Weakness', 3]}}},
                                     'bat': {'hp': 40, 'name': 'Bat Chan',
                                             'attacks': {'sonic_attack': {'phrase': 'Sonic Attack', 'block': 0, 'status': 'None', 'damage': 15, 'buff': 'None', 'heal': 0},
                                                         'resonate': {'phrase': 'Resonate', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Weakness', 2]}}}}}
                        case 2:
                            self.level_confs[i] = {
                                'level_3':
                                    {'player': {'hp': 100, 'columns': 7, 'energy': 5, 'rows': 4,
                                                'cards': {'air_chan': {'block': 5, 'buff': 'None', 'heal': 5, 'status': ['Weakness', 2], 'damage': 0},
                                                          'angel_chan': {'block': 0, 'buff': 'None', 'heal': 10, 'status': 'None', 'damage': 5},
                                                          'avatar_chan': {'block': 5, 'buff': ['Power', 1], 'heal': 5, 'status': ['Weakness', 1], 'damage': 5},
                                                          'earth_chan': {'block': 10, 'buff': ['Armor', 3], 'heal': 0, 'status': 'None', 'damage': 0},
                                                          'farquaad_chan': {'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Marked', 3], 'damage': 10},
                                                          'fire_chan': {'block': 0, 'buff': ['Power', 2], 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'jackie_chan': {'block': 10, 'buff': ['Energized', 1], 'heal': 0, 'status': ['Weakness', 2], 'damage': 0},
                                                          'jesus_chan': {'block': 0, 'buff': ['Clairvoyant', 2], 'heal': 15, 'status': 'None', 'damage': 0},
                                                          'oni_chan': {'block': 0, 'buff': ['Power', 2], 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'shrek_chan': {'block': 10, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                          'square_chan': {'block': 0, 'buff': ['Clairvoyant', 2], 'heal': 0, 'status': ['Marked', 3], 'damage': 0},
                                                          'un-chany_chan': {'block': 0, 'buff': ['Energized', 1], 'heal': 0, 'status': 'None', 'damage': 15},
                                                          'upsidedown_chan': {'block': 10, 'buff': ['Lifesteal', 2], 'heal': 0, 'status': 'None', 'damage': 5},
                                                          'water_chan': {'block': 0, 'buff': ['Regeneration', 5], 'heal': 10, 'status': 'None', 'damage': 0}}},
                                     'boss': {
                                         'moves': {'basic_1': {'phrases': ['You need to touch grass.', 'My son could beat you at this game.',
                                                                           'Easy choices hard life, hard choices easy life.',
                                                                           "It's only awkward if you make it awkward.", 'You have to build capacity.',
                                                                           "You chose that? Come on, that's crazy talk!!!", "Can't you be doing more?"],
                                                               'damage': 0, 'block': 0, 'status': ['disappointment', 1], 'buff': 'None', 'heal': 0},
                                                   'basic_2': {'phrases': ['Almost everything is a choice... including breathing!',
                                                                           'Reflect, reflect, REFLECT HARDER!!!', 'Face the monster... ME!',
                                                                           'Keep your head on a swivel!'],
                                                               'damage': 0, 'block': 0, 'status': ['Fear', 2], 'buff': 'None', 'heal': 0},
                                                   'special': {'phrases': ['Next time, just practice perfectly.', 'My record just increased :p'],
                                                               'damage': 999, 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0},
                                                   'death': {'phrases': ['Huh.', 'Looks like you did practice perfectly.', "Welp, I'll be on my way then.", '*leaves*'],
                                                             'damage': 0, 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0}},
                                         'hp': 200, 'name': 'Mr. Phone', 'phrases': {'intro': ['Did you write your TQP?']}},
                                     'enemies':
                                         {'flying': {'hp': 100, 'name': 'Flying Chan',
                                                     'attacks': {'swoop_in': {'phrase': 'Swoop In', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Fear', 2]},
                                                                 'claw_strike': {'phrase': 'Claw Strike', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 20},
                                                                 'fly_Up': {'phrase': 'Fly Up', 'damage': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'block': 25}}},
                                          'drowned': {'hp': 50, 'name': 'Drowned Chan',
                                                      'attacks': {
                                                          'drowned_glare': {'phrase': 'Drowned Glare', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Fear', 2]},
                                                          'bloated_breath': {'phrase': 'Bloated Breath', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0,
                                                                             'status': ['Vulnerable', 1]},
                                                          'corpse_explosion': {'phrase': 'Corpse Explosion', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': -50,
                                                                               'damage': 50}}},
                                          'big': {'hp': 150, 'name': 'Big Chan',
                                                  'attacks': {'big_smack': {'phrase': 'Biggus Smackus', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 20}}},
                                          'dark': {'hp': 60, 'name': 'Dark Chan',
                                                   'attacks': {'dark_orb': {'phrase': 'Dark Orb', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0, 'damage': 20},
                                                               'darkness': {'phrase': 'Darkness', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Weakness', 3]},
                                                               'curse': {'phrase': 'Dark Curse', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Vulnerable', 2]},
                                                               'dark_claw': {'phrase': 'Dark Claw', 'block': 0, 'status': 'None', 'buff': 'None', 'heal': 0, 'damage': 10}}},
                                          'goblin': {'hp': 50, 'name': 'Goblin Chan',
                                                     'attacks': {'evasive_maneuvers': {'phrase': 'Evasive Maneuvers', 'damage': 0, 'buff': 'None', 'heal': 0, 'status': 'None',
                                                                                       'block': 25},
                                                                 'tiny_stab': {'phrase': 'Tiny Stab', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 10},
                                                                 'hamstring': {'phrase': 'Hamstring', 'damage': 0, 'buff': 'None', 'heal': 0, 'block': 0,
                                                                               'status': ['Weakness', 3]}}},
                                          'bat': {'hp': 50, 'name': 'Bat Chan',
                                                  'attacks': {'sonic_attack': {'phrase': 'Sonic Attack', 'block': 0, 'status': 'None', 'damage': 20, 'buff': 'None', 'heal': 0},
                                                              'resonate': {'phrase': 'Resonate', 'damage': 0, 'block': 0, 'buff': 'None', 'heal': 0, 'status': ['Weakness', 2]},
                                                              'screech': {'phrase': 'Screech', 'block': 0, 'buff': 'None', 'heal': 0, 'status': 'None', 'damage': 15}}}}}}
            else:
                self.level_confs[i] = open(os.getcwd() + "/configuration/levels/" + filename + ".yml", "r")
            print(self.level_confs)

    def load_boss_confs(self):  # Run this after load_global_config()
        self.boss_confs = {}
        for i in self.bosses:
            filename = "level_" + str(i)
            if not os.path.exists(os.getcwd() + "/configuration/levels/" + filename + ".yml"):
                with open(os.getcwd() + "/configuration/levels/" + filename + ".yml", "w") as f:
                    self.boss_confs[str(i)] = f

    def load_media(self):
        self.menu_img = self.load_images_resize(os.getcwd() + "/resources/menus", (1600, 900))
        self.boss_card = self.load_images_resize(os.getcwd() + "/resources/menus/boss_cards", (1600, 900))
        # ----------------------------------------------------------------------------------------------------------------------------
        print(self.level_confs)
        self.image_dict = {
            a: (pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/chans/" + chan + ".png"), self.chan_card_size).convert(), chan)
            for a, chan in enumerate(self.level_confs[1]["player"]["cards"])}
        self.image_dict["card_back"] = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), self.chan_card_size)
        self.backgrounds = {"Card Game": pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/bliss.jpg").convert(), (1600, 900)),
                            1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/Chan_background.png").convert(),
                                                        (1600, 900)),
                            2: pg.transform.smoothscale(
                                pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/ms_g_non-siberia_background.jpg").convert(), (1600, 900)),
                            "siberia": pg.transform.smoothscale(
                                pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/ms_g_siberia_background.jpg").convert(), (1600, 900)),
                            3: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_03-mr_phone/mr_phone_background.jpg").convert(),
                                                        (1600, 900))}
        self.end_screens = (pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/lose_screen.png").convert(), (1600, 900)),
                            pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/win_screen.png").convert(), (1600, 900)))
        self.enemies_images = {name: pg.transform.smoothscale(pg.image.load(os.getcwd() + "\\resources\\" + name + ".png").convert(), (100, 100)) for
                               name in self.global_conf["level_1"]["enemies"]}
        self.f_hp_bar_hp = pg.font.Font(os.getcwd() + "\\resources\\EXEPixelPerfect.ttf", 125)
        self.f_hp_bar_name = pg.font.Font(os.getcwd() + "\\resources\\EXEPixelPerfect.ttf", 50)
        self.f_boss_text = pg.font.Font(os.getcwd() + "\\resources\\EXEPixelPerfect.ttf", 80)
        self.f_options_title = pg.font.Font(os.getcwd() + "\\resources\\Herculanum-Regular.ttf", 75)
        self.f_options_sub = pg.font.Font(os.getcwd() + "\\resources\\Herculanum-Regular.ttf", 40)
        self.face_images = {1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/devil_chan.png").convert_alpha(),
                                                        self.boss_face_size),
                            2: {filename[5:-4]: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/" + filename),
                                                                         self.boss_face_size).convert_alpha()
                                for filename in os.listdir(os.getcwd() + "/resources/boss_02-ms_g/") if filename.endswith(".png")},
                            3: {filename[6:-4]: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_03-mr_phone/" + filename),
                                                                         self.boss_face_size).convert_alpha()
                                for filename in os.listdir(os.getcwd() + "/resources/boss_03-mr_phone/") if filename.endswith(".png")}}

    def get_config(self):
        # print(self.player_hp, self.enable_music, self.enable_sfx, self.music_vol, self.sfx_vol,
        #       self.fps_show, self.fps_30, self.fps_60, self.fps_75, self.fps_165)
        return self.global_conf

    @staticmethod
    def load_audio_set(path_to_directory, extension):
        """
        Args:
            path_to_directory:string:
                Directory to audio files
            extension:string:
                File extension of audio files
        """
        audio_set = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith(extension):
                path = os.path.join(path_to_directory, filename)
                audio_set.append(pg.mixer.Sound(path))
        return audio_set

    @staticmethod
    def load_images(path_to_directory):
        """
        Args:
            path_to_directory:string:
                Directory of images
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.image.load(path).convert())
        return image_list

    @staticmethod
    def load_images_alpha(path_to_directory):
        """
        Args:
            path_to_directory:string:
                Directory of images
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.image.load(path).convert_alpha())
        return image_list

    @staticmethod
    def load_images_alpha_resize(path_to_directory, size):
        """
        Args:
            path_to_directory:string:
                Directory of images
            size::tuple:
                Desired new resolution
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.transform.smoothscale(pg.image.load(path), size).convert_alpha())
        return image_list

    @staticmethod
    def load_images_resize(path_to_directory, size):
        """
        Args:
            path_to_directory:string:
                Directory of images
            size::tuple:
                Desired new resolution
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.transform.smoothscale(pg.image.load(path), size).convert())
        return image_list

    @staticmethod
    def resize_images(images, size):
        """
        Args:
            images:list:
                List of images to be resized
            size:tuple:
                Resolution to resize image list to
        """
        lst = []
        for idx, i in enumerate(images):
            lst.append(pg.transform.smoothscale(i, size).convert_alpha())
        return lst
