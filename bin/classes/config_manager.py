import os

import pygame as pg
import yaml  # https://zetcode.com/python/yaml/


class Config(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # ----------------------------------------------------------------------------------------------------------------------------
        # Images
        self.img_menus = {}
        self.img_levels = {}
        self.img_cards = {}
        self.img_enemies = {}
        self.img_bosses = {}
        self.img_boss_select = {}
        self.img_end_screens = None
        self.img_ui = {}
        # ----------------------------------------------------------------------------------------------------------------------------
        # Fonts
        self.f_hp_bar_hp = None
        self.f_hp_bar_name = None
        self.f_boss_text = None
        self.f_options_title = None
        self.f_status = None
        self.f_intro = None
        self.f_regular = None
        self.f_regular_small = None
        self.f_stats = None
        self.f_block = None
        self.f_regular_big = None
        self.f_fps = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Settings
        # NOTE - AUDIO SETTINGS ARE LOCATED IN THE AUDIO CLASS & LOADED DURING BOOT
        self.fps_show = None
        self.FPS = 165
        self.fullscreen = None
        self.skip_intro = None
        self.fast_boot = None
        self.skip_enemies = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Other
        self.highest_level_beat = None
        self.last_level = None
        self.boss_face_size = None
        self.chan_card_size = None
        self.boss_face_size = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Config File Data
        self.global_conf = {}
        self.level_confs = {}
        self.boss_confs = {}
        # ----------------------------------------------------------------------------------------------------------------------------
        # Audio
        self.audio_menus = {}
        self.audio_completion = {}
        self.audio_card_game = {}
        self.audio_interact = {}
        self.audio_lvl_1 = {}
        self.audio_lvl_2 = {}
        self.audio_lvl_3 = {}
        # ----------------------------------------------------------------------------------------------------------------------------
        self.levels = 3
        self.bosses = ["devil_chan", "ms_g", "mr_phone"]

    @staticmethod
    def save_settings(new_dict):
        if new_dict is not None:
            with open(os.getcwd() + "/configuration/config.yml", "w") as f:
                yaml.dump(new_dict, f, sort_keys=False)

    def load_global_conf(self):
        if not os.path.exists(os.getcwd() + "/configuration/config.yml"):
            with open(os.getcwd() + "/configuration/config.yml", "w") as f:
                # Create config file with default values if it doesn't exist
                yaml.dump({'settings': {'audio': {'enable_music': True, 'enable_sfx': True, 'vol_music': 1.0, 'vol_sfx': 1.0}, 'fps': {'show': True, 'value': 165}, 'fullscreen': True, 'skip_intro': False, 'fast_boot': False, 'skip_enemies': True}, 'other': {'chan_card_size': [110, 165], 'boss_face_size': [500, 500], 'highest_level_beat': 1, 'last_level': 1}}, f, sort_keys=False)

        with open(os.getcwd() + "/configuration/config.yml", "r") as f:
            # Audio settings are found in the Audio class, and are loaded during boot
            self.global_conf = yaml.safe_load(f)  # Save .yml file data into variable
            self.fps_show = self.global_conf["settings"]["fps"]["show"]
            self.FPS = self.global_conf["settings"]["fps"]["value"]
            self.fullscreen = self.global_conf["settings"]["fullscreen"]
            self.skip_intro = self.global_conf["settings"]["skip_intro"]
            self.fast_boot = self.global_conf["settings"]["fast_boot"]
            self.boss_face_size = self.global_conf["other"]["boss_face_size"]
            self.chan_card_size = self.global_conf["other"]["chan_card_size"]
            self.highest_level_beat = self.global_conf["other"]["highest_level_beat"]
            self.last_level = self.global_conf["other"]["last_level"]
            self.skip_enemies = self.global_conf["settings"]["skip_enemies"]

    def load_level_confs(self):  # Run this after load_global_config() - Create files if they don't exist, and read from them
        for i in range(1, self.levels + 1):
            filename = "level_" + str(i)
            if not os.path.exists(os.getcwd() + "/configuration/levels/" + filename + ".yml"):
                with open(os.getcwd() + "/configuration/levels/" + filename + ".yml", "w") as f:
                    match i:
                        case 1:
                            yaml.dump({'enemies': {'bat': {'attacks': {'resonate': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Resonate', 'debuff': {'weakness': 1}}, 'sonic_attack': {'block': 0, 'buff': 'None', 'damage': 27, 'heal': 0, 'attack': 'Sonic Attack', 'debuff': 'None'}}, 'hp': 15, 'name': 'Bat Chan'}, 'big': {'attacks': {'big_smack': {'block': 15, 'buff': 'None', 'damage': 30, 'heal': 5, 'attack': 'Biggus Smackus', 'debuff': 'None'}}, 'hp': 69, 'name': 'Big Chan'}, 'dark': {'attacks': {'dark_curse': {'block': 10, 'buff': 'None', 'damage': 15, 'heal': 5, 'attack': 'Dark Curse', 'debuff': {'vulnerable': 1}}, 'dark_orb': {'block': 10, 'buff': 'None', 'damage': 25, 'heal': 0, 'attack': 'Dark Orb', 'debuff': 'None'}, 'darkness': {'block': 20, 'buff': 'None', 'damage': 5, 'heal': 15, 'attack': 'Darkness', 'debuff': {'weakness': 2}}}, 'hp': 50, 'name': 'Dark Chan'}, 'zombie': {'attacks': {'bloated_breath': {'block': 3, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Bloated Breath', 'debuff': {'vulnerable': 1}}, 'corpse_explosion': {'block': 0, 'buff': 'None', 'damage': 59, 'heal': -29, 'attack': 'Corpse Explosion', 'debuff': 'None'}, 'drowned_glare': {'block': 4, 'buff': 'None', 'damage': 0, 'heal': -3, 'attack': 'Drowned Glare', 'debuff': {'fear': 1}}}, 'hp': 30, 'name': 'Zombie Chan'}, 'scrambled': {'attacks': {'claw_strike': {'block': 10, 'buff': 'None', 'damage': 23, 'heal': 0, 'attack': 'Claw Strike', 'debuff': 'None'}, 'fly_up': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Fly Up', 'debuff': 'None'}, 'swoop_in': {'block': 4, 'buff': 'None', 'damage': 5, 'heal': 0, 'attack': 'Swoop In', 'debuff': {'fear': 1}}}, 'hp': 50, 'name': 'Scrambled Chan'}, 'goblin': {'attacks': {'evasive_maneuvers': {'block': 25, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Evasive Maneuvers', 'debuff': 'None'}, 'hamstring': {'block': 10, 'buff': 'None', 'damage': 20, 'heal': 0, 'attack': 'Hamstring', 'debuff': {'weakness': 2}}, 'poke': {'block': 10, 'buff': 'None', 'damage': 25, 'heal': 0, 'attack': 'Poke', 'debuff': 'None'}}, 'hp': 20, 'name': 'Goblin Chan'}, 'four': {'attacks': {'falsify_news': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 10, 'attack': 'Falsify News', 'debuff': {'weakness': 2}}, 'rousing_34': {'block': 0, 'buff': {'power': 2}, 'damage': 0, 'heal': 15, 'attack': 'Rousing 34', 'debuff': 'None'}, 'dox_threats': {'block': 0, 'buff': 'None', 'damage': 21, 'heal': 0, 'attack': 'Dox Threats', 'debuff': {'fear': 2}}}, 'hp': 20, 'name': '4 Chan'}, 'frying': {'attacks': {'burning_oil': {'block': 10, 'buff': 'None', 'damage': 12, 'heal': 5, 'attack': 'Burning Oil', 'debuff': {'wounded': 5}}, 'frying_shield': {'block': 20, 'buff': {'armor': 5}, 'damage': 0, 'heal': 0, 'attack': 'Frying Shield', 'debuff': {'wounded': 3}}, 'recuperate': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 15, 'attack': 'Recuperate', 'debuff': 'None'}}, 'hp': 50, 'name': 'Frying Chan'}, 'phrases': {'enemy_intro': {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'You have encountered a wild ---!!!', 'wait': 1.0}, 'enemy_player_death': {0: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 0.7, 'shake': [0, 0], 'text': '--- has defeated you!!!', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.05, 'fade_in': False, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [0, 0], 'text': "You're gonna have to try harder than that...", 'wait': 1.0}}, 'enemy_death': {'clear': True, 'delay': 0.04, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 2.0, 'shake': [0, 0], 'text': 'You strike down --- with a mighty slash!!!', 'wait': 1.0}}}, 'player': {'cards': {'air_chan': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 10, 'debuff': {'weakness': 2}, 'upgrades': {'flighty': {'block': 5, 'buff': {'energized': 1}, 'damage': 0, 'heal': 10, 'debuff': 'None'}}}, 'angel_chan': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None', 'upgrades': {'bright': {'block': 0, 'buff': {'regeneration': 5}, 'damage': 5, 'heal': 5, 'debuff': 'None'}}}, 'avatar_chan': {'block': 5, 'buff': {'power': 10}, 'damage': 15, 'heal': 5, 'debuff': {'weakness': 1}, 'upgrades': {'master': {'block': 5, 'buff': {'power': 1}, 'damage': 5, 'heal': 0, 'debuff': {'weakness': 1}}}}, 'earth_chan': {'block': 10, 'buff': {'armor': 5}, 'damage': 12, 'heal': 0, 'debuff': 'None', 'upgrades': {'tough': {'block': 5, 'buff': {'armor': 3}, 'damage': 0, 'heal': 0, 'debuff': 'None'}}}, 'farquaad_chan': {'block': 0, 'buff': 'None', 'damage': 28, 'heal': -12, 'debuff': {'marked': 3}, 'upgrades': {'despotic': {'block': 0, 'buff': {'armor': 5}, 'damage': -5, 'heal': 0, 'debuff': {'marked': 2}}}}, 'fire_chan': {'block': 0, 'buff': {'power': 2}, 'damage': 16, 'heal': 0, 'debuff': 'None', 'upgrades': {'burning': {'block': 0, 'buff': {'power': 1}, 'damage': 0, 'heal': 0, 'debuff': {'wounded': 5}}}}, 'jackie_chan': {'block': 10, 'buff': {'energized': 1}, 'damage': 5, 'heal': 0, 'debuff': {'weakness': 2}, 'upgrades': {'famous': {'block': 5, 'buff': {'clairvoyant': 1}, 'damage': 0, 'heal': 0, 'debuff': {'weakness': 1}}}}, 'jesus_chan': {'block': 5, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 15, 'debuff': 'None', 'upgrades': {'farsighted': {'block': 5, 'buff': {'energized': 1}, 'damage': 0, 'heal': 5, 'debuff': 'None'}}}, 'oni_chan': {'block': 3, 'buff': {'power': 2}, 'damage': 10, 'heal': 0, 'debuff': 'None', 'upgrades': {'vicious': {'block': 5, 'buff': 'None', 'damage': 5, 'heal': 0, 'debuff': {'vulnerable': 2}}}}, 'shrek_chan': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': 'None', 'upgrades': {'swampy': {'block': 0, 'buff': {'lifesteal': 1}, 'damage': 0, 'heal': 0, 'debuff': {'vulnerable': 2}}}}, 'square_chan': {'block': 0, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 0, 'debuff': {'marked': 3}, 'upgrades': {'symmetric': {'block': 0, 'buff': {'energized': 1}, 'damage': 0, 'heal': 0, 'debuff': {'wounded': 4}}}}, 'un-chany_chan': {'block': 0, 'buff': {'energized': 1}, 'damage': 25, 'heal': -25, 'debuff': 'None', 'upgrades': {'strange': {'block': 0, 'buff': 'None', 'damage': -5, 'heal': 10, 'debuff': {'vulnerable': 2}}}}, 'upsidedown_chan': {'block': 10, 'buff': {'lifesteal': 2}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'sinister': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'debuff': {'marked': 2}}}}, 'water_chan': {'block': 0, 'buff': {'regeneration': 5}, 'damage': 0, 'heal': 15, 'debuff': 'None', 'upgrades': {'raging': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': {'weakness': 2}}}}, 'snake_chan': {'block': 0, 'buff': {'weakness': 2}, 'damage': 0, 'heal': 5, 'debuff': {'wounded': 10}, 'upgrades': {'sly': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': 'None'}}}, 'bark_chan': {'block': 15, 'buff': {'armor': 5}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'natural': {'block': -5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None'}}}, 'uncanny_chan': {'block': 0, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'natural': {'block': -5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None'}}}}, 'columns': 3, 'energy': 3, 'hp': 50, 'rows': 4, 'base_deck': ['famous jackie_chan', 'famous jackie_chan', 'angel_chan', 'angel_chan', 'angel_chan', 'oni_chan', 'farquaad_chan', 'sinister upsidedown_chan']}}, f, sort_keys=False)
                        case 2:
                            yaml.dump({'enemies': {'bat': {'attacks': {'resonate': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Resonate', 'debuff': {'weakness': 1}}, 'sonic_attack': {'block': 0, 'buff': 'None', 'damage': 27, 'heal': 0, 'attack': 'Sonic Attack', 'debuff': 'None'}}, 'hp': 15, 'name': 'Bat Chan'}, 'big': {'attacks': {'big_smack': {'block': 15, 'buff': 'None', 'damage': 30, 'heal': 5, 'attack': 'Biggus Smackus', 'debuff': 'None'}}, 'hp': 69, 'name': 'Big Chan'}, 'dark': {'attacks': {'dark_curse': {'block': 10, 'buff': 'None', 'damage': 15, 'heal': 5, 'attack': 'Dark Curse', 'debuff': {'vulnerable': 1}}, 'dark_orb': {'block': 10, 'buff': 'None', 'damage': 25, 'heal': 0, 'attack': 'Dark Orb', 'debuff': 'None'}, 'darkness': {'block': 20, 'buff': 'None', 'damage': 5, 'heal': 15, 'attack': 'Darkness', 'debuff': {'weakness': 2}}}, 'hp': 50, 'name': 'Dark Chan'}, 'zombie': {'attacks': {'bloated_breath': {'block': 3, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Bloated Breath', 'debuff': {'vulnerable': 1}}, 'corpse_explosion': {'block': 0, 'buff': 'None', 'damage': 59, 'heal': -29, 'attack': 'Corpse Explosion', 'debuff': 'None'}, 'drowned_glare': {'block': 4, 'buff': 'None', 'damage': 0, 'heal': -3, 'attack': 'Drowned Glare', 'debuff': {'fear': 1}}}, 'hp': 30, 'name': 'Zombie Chan'}, 'scrambled': {'attacks': {'claw_strike': {'block': 10, 'buff': 'None', 'damage': 23, 'heal': 0, 'attack': 'Claw Strike', 'debuff': 'None'}, 'fly_up': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Fly Up', 'debuff': 'None'}, 'swoop_in': {'block': 4, 'buff': 'None', 'damage': 5, 'heal': 0, 'attack': 'Swoop In', 'debuff': {'fear': 1}}}, 'hp': 50, 'name': 'Scrambled Chan'}, 'goblin': {'attacks': {'evasive_maneuvers': {'block': 25, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Evasive Maneuvers', 'debuff': 'None'}, 'hamstring': {'block': 10, 'buff': 'None', 'damage': 20, 'heal': 0, 'attack': 'Hamstring', 'debuff': {'weakness': 2}}, 'poke': {'block': 10, 'buff': 'None', 'damage': 25, 'heal': 0, 'attack': 'Poke', 'debuff': 'None'}}, 'hp': 20, 'name': 'Goblin Chan'}, 'four': {'attacks': {'falsify_news': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 10, 'attack': 'Falsify News', 'debuff': {'weakness': 2}}, 'rousing_34': {'block': 0, 'buff': {'power': 2}, 'damage': 0, 'heal': 15, 'attack': 'Rousing 34', 'debuff': 'None'}, 'dox_threats': {'block': 0, 'buff': 'None', 'damage': 21, 'heal': 0, 'attack': 'Dox Threats', 'debuff': {'fear': 2}}}, 'hp': 20, 'name': '4 Chan'}, 'frying': {'attacks': {'burning_oil': {'block': 10, 'buff': 'None', 'damage': 12, 'heal': 5, 'attack': 'Burning Oil', 'debuff': {'wounded': 5}}, 'frying_shield': {'block': 20, 'buff': {'armor': 5}, 'damage': 0, 'heal': 0, 'attack': 'Frying Shield', 'debuff': {'wounded': 3}}, 'recuperate': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 15, 'attack': 'Recuperate', 'debuff': 'None'}}, 'hp': 50, 'name': 'Frying Chan'}, 'phrases': {'enemy_intro': {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'You have encountered a wild ---!!!', 'wait': 1.0}, 'enemy_player_death': {0: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 0.7, 'shake': [0, 0], 'text': '--- has defeated you!!!', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.05, 'fade_in': False, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [0, 0], 'text': "You're gonna have to try harder than that...", 'wait': 1.0}}, 'enemy_death': {'clear': True, 'delay': 0.04, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 2.0, 'shake': [0, 0], 'text': 'You clap --- with a mighty slash!!!', 'wait': 1.0}}}, 'player': {'cards': {'air_chan': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 10, 'debuff': {'weakness': 2}, 'upgrades': {'flighty': {'block': 5, 'buff': {'energized': 1}, 'damage': 0, 'heal': 10, 'debuff': 'None'}}}, 'angel_chan': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None', 'upgrades': {'bright': {'block': 0, 'buff': {'regeneration': 5}, 'damage': 5, 'heal': 5, 'debuff': 'None'}}}, 'avatar_chan': {'block': 5, 'buff': {'power': 10}, 'damage': 15, 'heal': 5, 'debuff': {'weakness': 1}, 'upgrades': {'master': {'block': 5, 'buff': {'power': 1}, 'damage': 5, 'heal': 0, 'debuff': {'weakness': 1}}}}, 'earth_chan': {'block': 10, 'buff': {'armor': 5}, 'damage': 12, 'heal': 0, 'debuff': 'None', 'upgrades': {'tough': {'block': 5, 'buff': {'armor': 3}, 'damage': 0, 'heal': 0, 'debuff': 'None'}}}, 'farquaad_chan': {'block': 0, 'buff': 'None', 'damage': 28, 'heal': -12, 'debuff': {'marked': 3}, 'upgrades': {'despotic': {'block': 0, 'buff': {'armor': 5}, 'damage': -5, 'heal': 0, 'debuff': {'marked': 2}}}}, 'fire_chan': {'block': 0, 'buff': {'power': 2}, 'damage': 16, 'heal': 0, 'debuff': 'None', 'upgrades': {'burning': {'block': 0, 'buff': {'power': 1}, 'damage': 0, 'heal': 0, 'debuff': {'wounded': 5}}}}, 'jackie_chan': {'block': 10, 'buff': {'energized': 1}, 'damage': 5, 'heal': 0, 'debuff': {'weakness': 2}, 'upgrades': {'famous': {'block': 5, 'buff': {'clairvoyant': 1}, 'damage': 0, 'heal': 0, 'debuff': {'weakness': 1}}}}, 'jesus_chan': {'block': 5, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 15, 'debuff': 'None', 'upgrades': {'farsighted': {'block': 5, 'buff': {'energized': 1}, 'damage': 0, 'heal': 5, 'debuff': 'None'}}}, 'oni_chan': {'block': 3, 'buff': {'power': 2}, 'damage': 10, 'heal': 0, 'debuff': 'None', 'upgrades': {'vicious': {'block': 5, 'buff': 'None', 'damage': 5, 'heal': 0, 'debuff': {'vulnerable': 2}}}}, 'shrek_chan': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': 'None', 'upgrades': {'swampy': {'block': 0, 'buff': {'lifesteal': 1}, 'damage': 0, 'heal': 0, 'debuff': {'vulnerable': 2}}}}, 'square_chan': {'block': 0, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 0, 'debuff': {'marked': 3}, 'upgrades': {'symmetric': {'block': 0, 'buff': {'energized': 1}, 'damage': 0, 'heal': 0, 'debuff': {'wounded': 4}}}}, 'un-chany_chan': {'block': 0, 'buff': {'energized': 1}, 'damage': 25, 'heal': -25, 'debuff': 'None', 'upgrades': {'strange': {'block': 0, 'buff': 'None', 'damage': -5, 'heal': 10, 'debuff': {'vulnerable': 2}}}}, 'upsidedown_chan': {'block': 10, 'buff': {'lifesteal': 2}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'sinister': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'debuff': {'marked': 2}}}}, 'water_chan': {'block': 0, 'buff': {'regeneration': 5}, 'damage': 0, 'heal': 15, 'debuff': 'None', 'upgrades': {'raging': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': {'weakness': 2}}}}, 'snake_chan': {'block': 0, 'buff': {'weakness': 2}, 'damage': 0, 'heal': 5, 'debuff': {'wounded': 10}, 'upgrades': {'sly': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': 'None'}}}, 'bark_chan': {'block': 15, 'buff': {'armor': 5}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'natural': {'block': -5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None'}}}, 'uncanny_chan': {'block': 0, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'natural': {'block': -5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None'}}}}, 'columns': 5, 'energy': 4, 'hp': 60, 'rows': 4, 'base_deck': ['farquaad_chan', 'farquaad_chan', 'sinister upsidedown_chan', 'angel_chan', 'angel_chan', 'air_chan', 'earth_chan', 'fire_chan', 'water_chan', 'avatar_chan']}}, f, sort_keys=False)
                        case 3:
                            yaml.dump({'enemies': {'bat': {'attacks': {'resonate': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Resonate', 'debuff': {'weakness': 1}}, 'sonic_attack': {'block': 0, 'buff': 'None', 'damage': 27, 'heal': 0, 'attack': 'Sonic Attack', 'debuff': 'None'}}, 'hp': 15, 'name': 'Bat Chan'}, 'big': {'attacks': {'big_smack': {'block': 15, 'buff': 'None', 'damage': 30, 'heal': 5, 'attack': 'Biggus Smackus', 'debuff': 'None'}}, 'hp': 69, 'name': 'Big Chan'}, 'dark': {'attacks': {'dark_curse': {'block': 10, 'buff': 'None', 'damage': 15, 'heal': 5, 'attack': 'Dark Curse', 'debuff': {'vulnerable': 1}}, 'dark_orb': {'block': 10, 'buff': 'None', 'damage': 25, 'heal': 0, 'attack': 'Dark Orb', 'debuff': 'None'}, 'darkness': {'block': 20, 'buff': 'None', 'damage': 5, 'heal': 15, 'attack': 'Darkness', 'debuff': {'weakness': 2}}}, 'hp': 50, 'name': 'Dark Chan'}, 'zombie': {'attacks': {'bloated_breath': {'block': 3, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Bloated Breath', 'debuff': {'vulnerable': 1}}, 'corpse_explosion': {'block': 0, 'buff': 'None', 'damage': 50, 'heal': -20, 'attack': 'Corpse Explosion', 'debuff': 'None'}, 'drowned_glare': {'block': 4, 'buff': 'None', 'damage': 0, 'heal': -3, 'attack': 'Drowned Glare', 'debuff': {'fear': 1}}}, 'hp': 30, 'name': 'Zombie Chan'}, 'scrambled': {'attacks': {'claw_strike': {'block': 10, 'buff': 'None', 'damage': 23, 'heal': 0, 'attack': 'Claw Strike', 'debuff': 'None'}, 'fly_up': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Fly Up', 'debuff': 'None'}, 'swoop_in': {'block': 4, 'buff': 'None', 'damage': 5, 'heal': 0, 'attack': 'Swoop In', 'debuff': {'fear': 1}}}, 'hp': 50, 'name': 'Scrambled Chan'}, 'goblin': {'attacks': {'evasive_maneuvers': {'block': 25, 'buff': 'None', 'damage': 0, 'heal': 0, 'attack': 'Evasive Maneuvers', 'debuff': 'None'}, 'hamstring': {'block': 10, 'buff': 'None', 'damage': 20, 'heal': 0, 'attack': 'Hamstring', 'debuff': {'weakness': 2}}, 'poke': {'block': 10, 'buff': 'None', 'damage': 25, 'heal': 0, 'attack': 'Poke', 'debuff': 'None'}}, 'hp': 20, 'name': 'Goblin Chan'}, 'four': {'attacks': {'falsify_news': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 10, 'attack': 'Falsify News', 'debuff': {'weakness': 2}}, 'rousing_34': {'block': 0, 'buff': {'power': 2}, 'damage': 0, 'heal': 15, 'attack': 'Rousing 34', 'debuff': 'None'}, 'dox_threats': {'block': 0, 'buff': 'None', 'damage': 21, 'heal': 0, 'attack': 'Dox Threats', 'debuff': {'fear': 2}}}, 'hp': 20, 'name': '4 Chan'}, 'frying': {'attacks': {'burning_oil': {'block': 10, 'buff': 'None', 'damage': 12, 'heal': 5, 'attack': 'Burning Oil', 'debuff': {'wounded': 5}}, 'frying_shield': {'block': 20, 'buff': {'armor': 5}, 'damage': 0, 'heal': 0, 'attack': 'Frying Shield', 'debuff': {'wounded': 3}}, 'recuperate': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 15, 'attack': 'Recuperate', 'debuff': 'None'}}, 'hp': 50, 'name': 'Frying Chan'}, 'phrases': {'enemy_intro': {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'You have encountered a wild ---!!!', 'wait': 1.0}, 'enemy_player_death': {0: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 0.7, 'shake': [0, 0], 'text': '--- has defeated you!!!', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.05, 'fade_in': False, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [0, 0], 'text': "You're gonna have to try harder than that...", 'wait': 1.0}}, 'enemy_death': {'clear': True, 'delay': 0.04, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 2.0, 'shake': [0, 0], 'text': 'You clap --- with a mighty slash!!!', 'wait': 1.0}}}, 'player': {'cards': {'air_chan': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 10, 'debuff': {'weakness': 2}, 'upgrades': {'flighty': {'block': 5, 'buff': {'energized': 1}, 'damage': 0, 'heal': 10, 'debuff': 'None'}}}, 'angel_chan': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None', 'upgrades': {'bright': {'block': 0, 'buff': {'regeneration': 5}, 'damage': 5, 'heal': 5, 'debuff': 'None'}}}, 'avatar_chan': {'block': 5, 'buff': {'power': 10}, 'damage': 15, 'heal': 5, 'debuff': {'weakness': 1}, 'upgrades': {'master': {'block': 5, 'buff': {'power': 1}, 'damage': 5, 'heal': 0, 'debuff': {'weakness': 1}}}}, 'earth_chan': {'block': 10, 'buff': {'armor': 5}, 'damage': 12, 'heal': 0, 'debuff': 'None', 'upgrades': {'tough': {'block': 5, 'buff': {'armor': 3}, 'damage': 0, 'heal': 0, 'debuff': 'None'}}}, 'farquaad_chan': {'block': 0, 'buff': 'None', 'damage': 28, 'heal': -12, 'debuff': {'marked': 3}, 'upgrades': {'despotic': {'block': 0, 'buff': {'armor': 5}, 'damage': -5, 'heal': 0, 'debuff': {'marked': 2}}}}, 'fire_chan': {'block': 0, 'buff': {'power': 2}, 'damage': 16, 'heal': 0, 'debuff': 'None', 'upgrades': {'burning': {'block': 0, 'buff': {'power': 1}, 'damage': 0, 'heal': 0, 'debuff': {'wounded': 5}}}}, 'jackie_chan': {'block': 10, 'buff': {'energized': 1}, 'damage': 5, 'heal': 0, 'debuff': {'weakness': 2}, 'upgrades': {'famous': {'block': 5, 'buff': {'clairvoyant': 1}, 'damage': 0, 'heal': 0, 'debuff': {'weakness': 1}}}}, 'jesus_chan': {'block': 5, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 15, 'debuff': 'None', 'upgrades': {'farsighted': {'block': 5, 'buff': {'energized': 1}, 'damage': 0, 'heal': 5, 'debuff': 'None'}}}, 'oni_chan': {'block': 3, 'buff': {'power': 2}, 'damage': 10, 'heal': 0, 'debuff': 'None', 'upgrades': {'vicious': {'block': 5, 'buff': 'None', 'damage': 5, 'heal': 0, 'debuff': {'vulnerable': 2}}}}, 'shrek_chan': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': 'None', 'upgrades': {'swampy': {'block': 0, 'buff': {'lifesteal': 1}, 'damage': 0, 'heal': 0, 'debuff': {'vulnerable': 2}}}}, 'square_chan': {'block': 0, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 0, 'debuff': {'marked': 3}, 'upgrades': {'symmetric': {'block': 0, 'buff': {'energized': 1}, 'damage': 0, 'heal': 0, 'debuff': {'wounded': 4}}}}, 'un-chany_chan': {'block': 0, 'buff': {'energized': 1}, 'damage': 25, 'heal': -25, 'debuff': 'None', 'upgrades': {'strange': {'block': 0, 'buff': 'None', 'damage': -5, 'heal': 10, 'debuff': {'vulnerable': 2}}}}, 'upsidedown_chan': {'block': 10, 'buff': {'lifesteal': 2}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'sinister': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'debuff': {'marked': 2}}}}, 'water_chan': {'block': 0, 'buff': {'regeneration': 5}, 'damage': 0, 'heal': 15, 'debuff': 'None', 'upgrades': {'raging': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': {'weakness': 2}}}}, 'snake_chan': {'block': 0, 'buff': {'weakness': 2}, 'damage': 0, 'heal': 5, 'debuff': {'wounded': 10}, 'upgrades': {'sly': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'debuff': 'None'}}}, 'bark_chan': {'block': 15, 'buff': {'armor': 5}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'natural': {'block': -5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None'}}}, 'uncanny_chan': {'block': 0, 'buff': {'clairvoyant': 2}, 'damage': 0, 'heal': 0, 'debuff': 'None', 'upgrades': {'natural': {'block': -5, 'buff': 'None', 'damage': 0, 'heal': 20, 'debuff': 'None'}}}}, 'columns': 7, 'energy': 5, 'hp': 69, 'rows': 4, 'base_deck': ['angel_chan', 'angel_chan', 'avatar_chan', 'earth_chan', 'farquaad_chan', 'farquaad_chan', 'fire_chan', 'famous jackie_chan', 'famous jackie_chan', 'oni_chan', 'shrek_chan', 'un-chany_chan', 'upsidedown_chan', 'water_chan']}}, f, sort_keys=False)

        for i in range(1, self.levels + 1):
            filename = "level_" + str(i)
            with open(os.getcwd() + "/configuration/levels/" + filename + ".yml", "r") as f:
                self.level_confs[i] = yaml.safe_load(f)

    def load_boss_confs(self):  # Run this after load_global_config()
        for i in self.bosses:
            if not os.path.exists(os.getcwd() + "/configuration/bosses/" + i + ".yml"):
                with open(os.getcwd() + "/configuration/bosses/" + i + ".yml", "w") as f:
                    match i:
                        case "devil_chan":
                            yaml.dump({'hp': 120, 'moves': {'basic': {0: {'block': 5, 'buff': 'None', 'damage': 28, 'heal': 0, 'debuff': 'None'}, 1: {'block': 10, 'buff': {'armor': 15}, 'damage': 23, 'heal': 0, 'debuff': {'weakness': 2}}, 2: {'block': 30, 'buff': {'power': 1}, 'damage': 10, 'heal': 10, 'debuff': {'vulnerable': 1}}}, 'special': {'block': 15, 'buff': {'lifesteal': 2}, 'damage': 40, 'heal': 25, 'debuff': 'None'}}, 'name': 'Devil Chan', 'phrases': {'boss_basic': {0: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'FOR MY LOST LOVE!!!', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'WORLD SHAKING EXPLOSION FIST!!!', 'wait': 1.0}, 2: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'NORTH STAR SPEAR!!!', 'wait': 1.0}, 3: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'MILLION SOUL BOMB!!!', 'wait': 1.0}, 4: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': 'BURNING SUN BEAM!!!', 'wait': 1.0}, 5: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [2, 2], 'text': '.2 ELECTRON VOLTS!!!', 'wait': 1.0}}, 'boss_death': {0: {'clear': False, 'delay': 0.05, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 1.0, 'shake': [3, 3], 'text': 'NOOOOOOO!!!', 'wait': 0}, 1: {'clear': True, 'delay': 0.06, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.4, 'shake': [15, 15], 'text': 'THIS IS BLASPHEMYYYYYY!!! *dies*', 'wait': 1.0}}, 'boss_player_death': {0: {'clear': False, 'delay': 0.05, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 1.0, 'shake': [3, 3], 'text': 'YEEESSSSS!!!', 'wait': 0}, 1: {'clear': True, 'delay': 0.06, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.4, 'shake': [15, 15], 'text': "THIS ISN'T BLASPHEMYYYYYY!!! *does not die*", 'wait': 1.0}}, 'boss_intro': {0: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 0.9, 'shake': [0, 0], 'text': 'ANGEL CHAN...', 'wait': 0}, 1: {'clear': True, 'delay': 0.09, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.3, 'shake': [5, 0], 'text': 'I LOVED YOU!', 'wait': 0.5}, 2: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.5, 'shake': [15, 20], 'text': 'HOW COULD YOU DO THIS TO ME!?', 'wait': 1.0}}, 'boss_special': {0: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [2, 2], 'text': "THAT'S A NEAT LITTLE HACK THAT I FOUND!", 'wait': 1.0}, 1: {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [2, 2], 'text': "WITH THIS HACK, I'LL TAKE YOUR HEALTH FOR MYSELF.", 'wait': 1.0}, 2: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [2, 2], 'text': "I HOPE YOU'RE PREPARED FOR THIS!", 'wait': 1.0}, 3: {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [2, 2], 'text': "YOU KNOW, I'M SOMETHING OF A SCIENTIST MYSELF.", 'wait': 1.0}}}}, f)
                        case "ms_g":
                            yaml.dump({'hp': 160, 'moves': {'basic': {0: {'block': 20, 'buff': 'None', 'damage': 20, 'heal': 0, 'debuff': {'vulnerable': 1}}, 1: {'block': 25, 'buff': 'None', 'damage': 15, 'heal': 0, 'debuff': {'weakness': 2}}, 2: {'block': 30, 'buff': 'None', 'damage': 5, 'heal': 10, 'debuff': 'None'}}, 'siberia': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 40, 'debuff': 'None'}}, 'name': 'Ms. G', 'phrases': {'boss_basic': {0: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [15, 15], 'text': 'For Sean!', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': "Don't ask me, use your brain.", 'wait': 1.0}, 2: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'I have WELHpon *pulls out a meter stick*', 'wait': 1.0}, 3: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Do it on repl.it!!!', 'wait': 1.0}}, 'boss_siberia': {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [0, 0], 'text': 'You!!! How did you escape Siberia!?', 'wait': 1.0}, 'boss_death': {'clear': False, 'delay': 0.05, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'why must you use... list comphrehension... *dies*', 'wait': 0}, 'boss_player_death': {'clear': False, 'delay': 0.05, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Your only flaw was not using list comprehension.', 'wait': 0}, 'boss_intro': {0: {'clear': False, 'delay': 0.06, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 0.9, 'shake': [0, 0], 'text': 'Hello Sean!', 'wait': 0}, 1: {'clear': True, 'delay': 0.09, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.3, 'shake': [0, 0], 'text': 'How are you doing?', 'wait': 0.5}, 2: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.5, 'shake': [0, 0], 'text': "Wait, you're not Sean!", 'wait': 1.0}}}}, f, sort_keys=False)
                        case "mr_phone":
                            yaml.dump({'hp': 200, 'moves': {'basic': {0: {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'debuff': {'disappointment': 1}}, 1: {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'debuff': {'fear': 2}}}, 'special': {'block': 0, 'buff': 'None', 'damage': 69420, 'heal': 0, 'debuff': 'None'}}, 'name': 'Mr. Phone', 'phrases': {'boss_basic': {0: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'You need to touch grass.', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'My son could beat you at this game.', 'wait': 1.0}, 2: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Easy choices hard life, hard choices easy life.', 'wait': 1.0}, 3: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': "It's only awkward if you make it awkward.", 'wait': 1.0}, 4: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'You have to build capacity.', 'wait': 1.0}, 5: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': "You chose that? Come on, that's crazy talk!!!", 'wait': 1.0}, 6: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': "Can't you be doing more?", 'wait': 1.0}, 7: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Almost everything is a choice... including breathing!', 'wait': 1.0}, 8: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Reflect, reflect, REFLECT HARDER!!!', 'wait': 1.0}, 9: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Face the monster... ME!', 'wait': 1.0}, 10: {'clear': True, 'delay': 0.07, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Keep your head on a swivel!', 'wait': 1.0}}, 'boss_death': {0: {'clear': False, 'delay': 0.05, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Huh. Looks like you did practice perfectly.', 'wait': 0}, 1: {'clear': True, 'delay': 0.06, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.4, 'shake': [0, 0], 'text': "Welp, I'll be on my way then.", 'wait': 1.0}, 2: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [0, 0], 'text': '*leaves*', 'wait': 1.0}}, 'boss_player_death': {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Remember, make your TQPs.', 'wait': 0}, 'boss_intro': {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 0.9, 'shake': [0, 0], 'text': 'Did you write your TQPs?', 'wait': 0}, 'boss_special': {0: {'clear': True, 'delay': 0.06, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [0, 0], 'text': 'Next time, just practice perfectly.', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.05, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.3, 'shake': [0, 0], 'text': 'My record just increased :p', 'wait': 1.0}}}}, f, sort_keys=False)
        for i in self.bosses:
            with open(os.getcwd() + "/configuration/bosses/" + i + ".yml", "r") as f:
                self.boss_confs[i] = yaml.safe_load(f)

    def load_img_menus(self):
        self.img_menus = self.load_images_dict(os.getcwd() + "/resources/menus", (self.width, self.height))

    def load_img_boss_select(self):  # Level select images
        self.img_boss_select = self.load_images_resize(os.getcwd() + "/resources/menus/boss_cards", (self.width, self.height))

    def load_chan_cards(self):
        self.img_cards = self.load_images_dict(os.getcwd() + "/resources/chan_cards/", self.chan_card_size)
        self.img_cards["card_back"] = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), self.chan_card_size)

    def load_img_backgrounds(self):
        self.img_levels = {
            1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_1/background.png").convert(), (self.width, self.height)),
            2: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_2/background.png").convert(), (self.width, self.height)),
            3: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_3/background.jpg").convert(), (self.width, self.height)),
            "siberia": pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_2/siberia.jpg").convert(), (self.width, self.height)),
            "card_game": pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/menus/bliss.png").convert(), (self.width, self.height))
        }

    def load_img_bosses(self):
        self.img_bosses = {
            1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_1/boss/devil_chan.png").convert_alpha(), self.boss_face_size),
            2: self.load_images_dict(os.getcwd() + "/resources/level_2/boss/", self.boss_face_size, True, "ms_g_"),
            3: self.load_images_dict(os.getcwd() + "/resources/level_3/boss/", self.boss_face_size, True, "phone_")
        }

    def load_img_enemies(self):
        self.img_enemies = {level: {} for level in range(1, 3)}
        self.img_enemies = self.load_images_dict(os.getcwd() + "/resources/chan_enemies/", self.boss_face_size, True, "_chan")

    def load_img_end_screens(self):
        self.img_end_screens = (pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/lose_screen.png").convert(), (self.width, self.height)),
                                pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/win_screen.png").convert(), (self.width, self.height)))

    def load_img_ui(self):
        self.img_ui = self.load_images_dict(os.getcwd() + "/resources/ui/", (75, 75), True)
        self.img_ui["buff"] = self.load_images_dict(os.getcwd() + "/resources/ui/buffs", (30, 30), True, "", False)
        self.img_ui["debuff"] = self.load_images_dict(os.getcwd() + "/resources/ui/debuffs", (30, 30), True, "", False)
        self.img_ui["block"] = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/ui/block.png").convert_alpha(), (45, 45))

    def load_fonts(self):
        self.f_hp_bar_hp = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 125)
        self.f_boss_text = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 80)
        self.f_hp_bar_name = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 50)
        self.f_status = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 45)
        self.f_intro = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 35)
        self.f_stats = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 30)
        self.f_regular_big = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 100)
        self.f_options_title = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 75)
        self.f_regular = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 50)
        self.f_regular_small = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 40)
        self.f_fps = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 30)

    def load_audio_menu(self):
        self.audio_menus = self.load_audio_dict(os.getcwd() + "/resources/audio/")

    def load_audio_completion(self):
        self.audio_completion = self.load_audio_dict(os.getcwd() + "/resources/audio/completion/")

    def load_audio_card_game(self):
        self.audio_card_game = self.load_audio_dict(os.getcwd() + "/resources/audio/card_game/")
        self.audio_card_game["attack_full_block"] = self.load_audio_set(os.getcwd() + "/resources/audio/card_game/attack_full_block/", "wav")
        self.audio_card_game["player_heal"] = self.load_audio_set(os.getcwd() + "/resources/audio/card_game/player_heal/", "wav")

    def load_audio_interact(self):
        self.audio_interact = self.load_audio_dict(os.getcwd() + "/resources/audio/interact/")

    def load_audio_lvl_1(self):
        self.audio_lvl_1 = self.load_audio_dict(os.getcwd() + "/resources/audio/level_1/")

    def load_audio_lvl_2(self):
        self.audio_lvl_2 = self.load_audio_dict(os.getcwd() + "/resources/audio/level_2/")

    def load_audio_lvl_3(self):
        self.audio_lvl_3 = self.load_audio_dict(os.getcwd() + "/resources/audio/level_3/")

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
    def load_images_dict(path_to_directory, resize=None, alpha=False, exclude="", smooth=True):
        """
        Args:
            path_to_directory:string:
                Directory of images
            resize:tuple:
                Size to resize images to
            alpha:boolean:
                Whether to convert the image to alpha or not
            exclude:string:
                String of characters not wanted in the keys
            smooth:string:
                Whether to use smooth scale or not
        """
        image_dict = {}
        name = None
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                path = os.path.join(path_to_directory, filename)
                if resize is not None:
                    image = pg.transform.smoothscale(pg.image.load(path), resize) if smooth else pg.transform.scale(pg.image.load(path), resize)
                else:
                    image = pg.image.load(path)
                if alpha:
                    name = (os.path.basename(filename).split(".")[0]).lower()
                    image_dict[name.replace(exclude, "")] = image.convert_alpha()
                else:
                    name = (os.path.basename(filename).split(".")[0]).lower()
                    image_dict[name.replace(exclude, "")] = image.convert()
        return image_dict

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
    def load_audio_dict(path_to_directory, exclude=""):
        """
        Args:
            path_to_directory:string:
                Directory of images
            exclude:string:
                String of characters not wanted in the keys
        """
        audio_dict = {}
        name = None
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.ogg'):
                path = os.path.join(path_to_directory, filename)
                name = (os.path.basename(filename).split(".")[0]).lower()
                audio_dict[name.replace(exclude, "")] = pg.mixer.Sound(path)
        return audio_dict
