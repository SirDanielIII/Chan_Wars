import yaml  # https://zetcode.com/python/yaml/
import os
import pygame as pg


# Note: [DEVIL CHAN ONLY] The values in Special Attack goes like [Attack Type, Damage, Heal]

class Config(object):
    def __init__(self):
        # ----------------------------------------------------------------------------------------------------------------------------
        # Images
        self.img_menus = {}
        self.img_levels = {}
        self.img_chans = {}
        self.img_enemies = {}
        self.img_bosses = {}
        self.img_boss_cards = {}
        self.img_end_screens = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Fonts
        self.f_hp_bar_hp = None
        self.f_hp_bar_name = None
        self.f_boss_text = None
        self.f_options_title = None
        self.f_regular = None
        self.f_regular_small = None
        self.f_regular_big = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Settings
        self.enable_music = None
        self.enable_sfx = None
        self.music_vol = None
        self.sfx_vol = None
        self.fps_show = None
        self.fps_value = 165  # Needs to have a value set due to boot menu
        self.levels = 3
        self.bosses = ["devil_chan", "ms_g", "mr_phone"]
        # ----------------------------------------------------------------------------------------------------------------------------
        # Other
        self.highest_level_beat = None
        self.boss_face_size = None
        self.chan_card_size = None
        self.boss_face_size = None
        # ----------------------------------------------------------------------------------------------------------------------------
        # Config File Data
        self.global_conf = {}
        self.level_confs = {}
        self.boss_confs = {}

    def load_global_conf(self):
        if not os.path.exists(os.getcwd() + "/configuration/config.yml"):
            with open(os.getcwd() + "/configuration/config.yml", "w") as f:
                # Create config file with default values if it doesn't exist
                yaml.dump({'settings': {'audio': {'enable_music': True, 'enable_sfx': True, 'music_vol': 1.0, 'sfx_vol': 1.0},
                                        'fps': {'show': False, 'value': 165}, 'fullscreen': False},
                           'other': {'levels': 3, 'bosses': ['devil_chan', 'mr_phone', 'ms_g'], 'chan_card_size': [120, 180],
                                     'boss_face_size': [500, 500], 'highest_level_beat': 0}}, f)

        with open(os.getcwd() + "/configuration/config.yml", "r") as f:
            self.global_conf = yaml.safe_load(f)  # Save .yml file data into variable
            self.enable_music = self.global_conf["settings"]["audio"]["enable_music"]
            self.enable_sfx = self.global_conf["settings"]["audio"]["enable_sfx"]
            self.music_vol = self.global_conf["settings"]["audio"]["music_vol"]
            self.sfx_vol = self.global_conf["settings"]["audio"]["sfx_vol"]
            self.fps_show = self.global_conf["settings"]["fps"]["show"]
            self.fps_value = self.global_conf["settings"]["fps"]["value"]
            self.highest_level_beat = self.global_conf["other"]["highest_level_beat"]
            self.boss_face_size = self.global_conf["other"]["boss_face_size"]
            self.chan_card_size = self.global_conf["other"]["chan_card_size"]

    def load_level_confs(self):  # Run this after load_global_config() - Create files if they don't exist, and read from them
        for i in range(1, self.levels + 1):
            filename = "level_" + str(i)
            if not os.path.exists(os.getcwd() + "/configuration/levels/" + filename + ".yml"):
                with open(os.getcwd() + "/configuration/levels/" + filename + ".yml", "w") as f:
                    match i:
                        case 1:
                            yaml.dump({'enemies': {'bat': {'attacks': {'resonate': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Resonate', 'status': {'Weakness': 1}}, 'sonic_attack': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Sonic Attack', 'status': 'None'}}, 'hp': 40, 'name': 'Bat Chan'}, 'big': {'attacks': {'big_smack': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrase': 'Biggus Smackus', 'status': 'None'}}, 'hp': 75, 'name': 'Big Chan'}, 'dark': {'attacks': {'dark_curse': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Dark Curse', 'status': {'Vulnerable': 1}}, 'dark_orb': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Dark Orb', 'status': 'None'}, 'darkness': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Darkness', 'status': {'Weakness': 2}}}, 'hp': 40, 'name': 'Dark Chan'}, 'drowned': {'attacks': {'bloated_breath': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Bloated Breath', 'status': {'Vulnerable': 1}}, 'corpse_explosion': {'block': 0, 'buff': 'None', 'damage': 25, 'heal': -30, 'phrase': 'Corpse Explosion', 'status': 'None'}, 'drowned_glare': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Drowned Glare', 'status': {'Fear': 1}}}, 'hp': 30, 'name': 'Drowned Chan'}, 'flying': {'attacks': {'claw_strike': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Claw Strike', 'status': 'None'}, 'fly_up': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Fly Up', 'status': 'None'}, 'swoop_in': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Swoop In', 'status': {'Fear': 1}}}, 'hp': 50, 'name': 'Flying Chan'}, 'goblin': {'attacks': {'evasive_maneuvers': {'block': 10, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Evasive Maneuvers', 'status': 'None'}, 'hamstring': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Hamstring', 'status': {'Weakness': 2}}, 'tiny_stab': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Tiny Stab', 'status': 'None'}}, 'hp': 30, 'name': 'Goblin Chan'}}, 'player': {'cards': {'air_chan': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 5, 'status': {'Weakness': 2}, 'upgrades': {'flighty': {'block': 5, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 10, 'status': 'None'}}}, 'angel_chan': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'status': 'None', 'upgrades': {'bright': {'block': 0, 'buff': {'Regeneration': 5}, 'damage': 5, 'heal': 5, 'status': 'None'}}}, 'avatar_chan': {'block': 5, 'buff': {'Power': 1}, 'damage': 5, 'heal': 5, 'status': {'Weakness': 1}, 'upgrades': {'master': {'block': 5, 'buff': {'Power': 1}, 'damage': 5, 'heal': 0, 'status': {'Weakness': 1}}}}, 'earth_chan': {'block': 10, 'buff': {'Armor': 3}, 'damage': 0, 'heal': 0, 'status': 'None', 'upgrades': {'tough': {'block': 5, 'buff': {'Armor': 3}, 'damage': 0, 'heal': 0, 'status': 'None'}}}, 'farquaad_chan': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': {'Marked': 3}, 'upgrades': {'despotic': {'block': 0, 'buff': {'Armor': 5}, 'damage': -5, 'heal': 0, 'status': {'Marked': 2}}}}, 'fire_chan': {'block': 0, 'buff': {'Power': 2}, 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'burning': {'block': 0, 'buff': {'Power': 1}, 'damage': 0, 'heal': 0, 'status': {'Pained': 5}}}}, 'jackie_chan': {'block': 10, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 0, 'status': {'Weakness': 2}, 'upgrades': {'famous': {'block': 5, 'buff': {'Clairvoyant': 1}, 'damage': 0, 'heal': 0, 'status': {'Weakness': 1}}}}, 'jesus_chan': {'block': 0, 'buff': {'Clairvoyant': 2}, 'damage': 0, 'heal': 15, 'status': 'None', 'upgrades': {'farsighted': {'block': 5, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 5, 'status': 'None'}}}, 'oni_chan': {'block': 0, 'buff': {'Power': 2}, 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'vicious': {'block': 5, 'buff': 'None', 'damage': 5, 'heal': 0, 'status': {'Vulnerable': 2}}}}, 'shrek_chan': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'swampy': {'block': 0, 'buff': {'Lifesteal': 1}, 'damage': 0, 'heal': 0, 'status': {'Vulnerable': 2}}}}, 'square_chan': {'block': 0, 'buff': {'Clairvoyant': 2}, 'damage': 0, 'heal': 0, 'status': {'Marked': 3}, 'upgrades': {'symmetric': {'block': 0, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 0, 'status': {'Pained': 4}}}}, 'un-chany_chan': {'block': 0, 'buff': {'Energized': 1}, 'damage': 15, 'heal': 0, 'status': 'None', 'upgrades': {'strange': {'block': 0, 'buff': 'None', 'damage': -5, 'heal': 10, 'status': {'Vulnerable': 2}}}}, 'upsidedown_chan': {'block': 10, 'buff': {'Lifesteal': 2}, 'damage': 5, 'heal': 0, 'status': 'None', 'upgrades': {'sinister': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'status': {'Marked': 2}}}}, 'water_chan': {'block': 0, 'buff': {'Regeneration': 5}, 'damage': 0, 'heal': 10, 'status': 'None', 'upgrades': {'raging': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': {'Weakness': 2}}}}}, 'columns': 3, 'energy': 3, 'hp': 50, 'rows': 4}}, f)
                        case 2:
                            yaml.dump({'enemies': {'bat': {'attacks': {'resonate': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Resonate', 'status': {'Weakness': 2}}, 'sonic_attack': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrase': 'Sonic Attack', 'status': 'None'}}, 'hp': 40, 'name': 'Bat Chan'}, 'big': {'attacks': {'big_smack': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrase': 'Biggus Smackus', 'status': 'None'}}, 'hp': 100, 'name': 'Big Chan'}, 'dark': {'attacks': {'curse': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Dark Curse', 'status': {'Vulnerable': 1}}, 'dark_orb': {'block': 0, 'buff': 'None', 'damage': 20, 'heal': 0, 'phrase': 'Dark Orb', 'status': 'None'}, 'darkness': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Darkness', 'status': {'Weakness': 2}}}, 'hp': 50, 'name': 'Dark Chan'}, 'drowned': {'attacks': {'bloated_breath': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Bloated Breath', 'status': {'Vulnerable': 1}}, 'corpse_explosion': {'block': 0, 'buff': 'None', 'damage': 35, 'heal': -40, 'phrase': 'Corpse Explosion', 'status': 'None'}, 'drowned_glare': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Drowned Glare', 'status': {'Fear': 2}}}, 'hp': 40, 'name': 'Drowned Chan'}, 'flying': {'attacks': {'claw_strike': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrase': 'Claw Strike', 'status': 'None'}, 'fly_Up': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Fly Up', 'status': 'None'}, 'swoop_in': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Swoop In', 'status': {'Fear': 2}}}, 'hp': 75, 'name': 'Flying Chan'}, 'goblin': {'attacks': {'evasive_maneuvers': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Evasive Maneuvers', 'status': 'None'}, 'hamstring': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Hamstring', 'status': {'Weakness': 3}}, 'tiny_stab': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Tiny Stab', 'status': 'None'}}, 'hp': 35, 'name': 'Goblin Chan'}}, 'player': {'cards': {'air_chan': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 5, 'status': {'Weakness': 2}, 'upgrades': {'flighty': {'block': 5, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 10, 'status': 'None'}}}, 'angel_chan': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'status': 'None', 'upgrades': {'bright': {'block': 0, 'buff': {'Regeneration': 5}, 'damage': 5, 'heal': 5, 'status': 'None'}}}, 'avatar_chan': {'block': 5, 'buff': {'Power': 1}, 'damage': 5, 'heal': 5, 'status': {'Weakness': 1}, 'upgrades': {'master': {'block': 5, 'buff': {'Power': 1}, 'damage': 5, 'heal': 0, 'status': {'Weakness': 1}}}}, 'earth_chan': {'block': 10, 'buff': {'Armor': 3}, 'damage': 0, 'heal': 0, 'status': 'None', 'upgrades': {'tough': {'block': 5, 'buff': {'Armor': 3}, 'damage': 0, 'heal': 0, 'status': 'None'}}}, 'farquaad_chan': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': {'Marked': 3}, 'upgrades': {'despotic': {'block': 0, 'buff': {'Armor': 5}, 'damage': -5, 'heal': 0, 'status': {'Marked': 2}}}}, 'fire_chan': {'block': 0, 'buff': {'Power': 2}, 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'burning': {'block': 0, 'buff': {'Power': 1}, 'damage': 0, 'heal': 0, 'status': {'Pained': 5}}}}, 'jackie_chan': {'block': 10, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 0, 'status': {'Weakness': 2}, 'upgrades': {'famous': {'block': 5, 'buff': {'Clairvoyant': 1}, 'damage': 0, 'heal': 0, 'status': {'Weakness': 1}}}}, 'jesus_chan': {'block': 0, 'buff': {'Clairvoyant': 2}, 'damage': 0, 'heal': 15, 'status': 'None', 'upgrades': {'farsighted': {'block': 5, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 5, 'status': 'None'}}}, 'oni_chan': {'block': 0, 'buff': {'Power': 2}, 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'vicious': {'block': 5, 'buff': 'None', 'damage': 5, 'heal': 0, 'status': {'Vulnerable': 2}}}}, 'shrek_chan': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'swampy': {'block': 0, 'buff': {'Lifesteal': 1}, 'damage': 0, 'heal': 0, 'status': {'Vulnerable': 2}}}}, 'square_chan': {'block': 0, 'buff': {'Clairvoyant': 2}, 'damage': 0, 'heal': 0, 'status': {'Marked': 3}, 'upgrades': {'symmetric': {'block': 0, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 0, 'status': {'Pained': 4}}}}, 'un-chany_chan': {'block': 0, 'buff': {'Energized': 1}, 'damage': 15, 'heal': 0, 'status': 'None', 'upgrades': {'strange': {'block': 0, 'buff': 'None', 'damage': -5, 'heal': 10, 'status': {'Vulnerable': 2}}}}, 'upsidedown_chan': {'block': 10, 'buff': {'Lifesteal': 2}, 'damage': 5, 'heal': 0, 'status': 'None', 'upgrades': {'sinister': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'status': {'Marked': 2}}}}, 'water_chan': {'block': 0, 'buff': {'Regeneration': 5}, 'damage': 0, 'heal': 10, 'status': 'None', 'upgrades': {'raging': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': {'Weakness': 2}}}}}, 'columns': 5, 'energy': 4, 'hp': 75, 'rows': 4}}, f)
                        case 3:
                            yaml.dump({'enemies': {'bat': {'attacks': {'resonate': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Resonate', 'status': {'Weakness': 2}}, 'screech': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrase': 'Screech', 'status': 'None'}, 'sonic_attack': {'block': 0, 'buff': 'None', 'damage': 20, 'heal': 0, 'phrase': 'Sonic Attack', 'status': 'None'}}, 'hp': 50, 'name': 'Bat Chan'}, 'big': {'attacks': {'big_smack': {'block': 0, 'buff': 'None', 'damage': 20, 'heal': 0, 'phrase': 'Biggus Smackus', 'status': 'None'}}, 'hp': 150, 'name': 'Big Chan'}, 'dark': {'attacks': {'curse': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Dark Curse', 'status': {'Vulnerable': 2}}, 'dark_claw': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Dark Claw', 'status': 'None'}, 'dark_orb': {'block': 0, 'buff': 'None', 'damage': 20, 'heal': 0, 'phrase': 'Dark Orb', 'status': 'None'}, 'darkness': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Darkness', 'status': {'Weakness': 3}}}, 'hp': 60, 'name': 'Dark Chan'}, 'drowned': {'attacks': {'bloated_breath': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Bloated Breath', 'status': {'Vulnerable': 1}}, 'corpse_explosion': {'block': 0, 'buff': 'None', 'damage': 50, 'heal': -50, 'phrase': 'Corpse Explosion', 'status': 'None'}, 'drowned_glare': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Drowned Glare', 'status': {'Fear': 2}}}, 'hp': 50, 'name': 'Drowned Chan'}, 'flying': {'attacks': {'claw_strike': {'block': 0, 'buff': 'None', 'damage': 20, 'heal': 0, 'phrase': 'Claw Strike', 'status': 'None'}, 'fly_Up': {'block': 25, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Fly Up', 'status': 'None'}, 'swoop_in': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Swoop In', 'status': {'Fear': 2}}}, 'hp': 100, 'name': 'Flying Chan'}, 'goblin': {'attacks': {'evasive_maneuvers': {'block': 25, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Evasive Maneuvers', 'status': 'None'}, 'hamstring': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrase': 'Hamstring', 'status': {'Weakness': 3}}, 'tiny_stab': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'phrase': 'Tiny Stab', 'status': 'None'}}, 'hp': 50, 'name': 'Goblin Chan'}}, 'player': {'cards': {'air_chan': {'block': 5, 'buff': 'None', 'damage': 0, 'heal': 5, 'status': {'Weakness': 2}, 'upgrades': {'flighty': {'block': 5, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 10, 'status': 'None'}}}, 'angel_chan': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'status': 'None', 'upgrades': {'bright': {'block': 0, 'buff': {'Regeneration': 5}, 'damage': 5, 'heal': 5, 'status': 'None'}}}, 'avatar_chan': {'block': 5, 'buff': {'Power': 1}, 'damage': 5, 'heal': 5, 'status': {'Weakness': 1}, 'upgrades': {'master': {'block': 5, 'buff': {'Power': 1}, 'damage': 5, 'heal': 0, 'status': {'Weakness': 1}}}}, 'earth_chan': {'block': 10, 'buff': {'Armor': 3}, 'damage': 0, 'heal': 0, 'status': 'None', 'upgrades': {'tough': {'block': 5, 'buff': {'Armor': 3}, 'damage': 0, 'heal': 0, 'status': 'None'}}}, 'farquaad_chan': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': {'Marked': 3}, 'upgrades': {'despotic': {'block': 0, 'buff': {'Armor': 5}, 'damage': -5, 'heal': 0, 'status': {'Marked': 2}}}}, 'fire_chan': {'block': 0, 'buff': {'Power': 2}, 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'burning': {'block': 0, 'buff': {'Power': 1}, 'damage': 0, 'heal': 0, 'status': {'Pained': 5}}}}, 'jackie_chan': {'block': 10, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 0, 'status': {'Weakness': 2}, 'upgrades': {'famous': {'block': 5, 'buff': {'Clairvoyant': 1}, 'damage': 0, 'heal': 0, 'status': {'Weakness': 1}}}}, 'jesus_chan': {'block': 0, 'buff': {'Clairvoyant': 2}, 'damage': 0, 'heal': 15, 'status': 'None', 'upgrades': {'farsighted': {'block': 5, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 5, 'status': 'None'}}}, 'oni_chan': {'block': 0, 'buff': {'Power': 2}, 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'vicious': {'block': 5, 'buff': 'None', 'damage': 5, 'heal': 0, 'status': {'Vulnerable': 2}}}}, 'shrek_chan': {'block': 10, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': 'None', 'upgrades': {'swampy': {'block': 0, 'buff': {'Lifesteal': 1}, 'damage': 0, 'heal': 0, 'status': {'Vulnerable': 2}}}}, 'square_chan': {'block': 0, 'buff': {'Clairvoyant': 2}, 'damage': 0, 'heal': 0, 'status': {'Marked': 3}, 'upgrades': {'symmetric': {'block': 0, 'buff': {'Energized': 1}, 'damage': 0, 'heal': 0, 'status': {'Pained': 4}}}}, 'un-chany_chan': {'block': 0, 'buff': {'Energized': 1}, 'damage': 15, 'heal': 0, 'status': 'None', 'upgrades': {'strange': {'block': 0, 'buff': 'None', 'damage': -5, 'heal': 10, 'status': {'Vulnerable': 2}}}}, 'upsidedown_chan': {'block': 10, 'buff': {'Lifesteal': 2}, 'damage': 5, 'heal': 0, 'status': 'None', 'upgrades': {'sinister': {'block': 0, 'buff': 'None', 'damage': 5, 'heal': 10, 'status': {'Marked': 2}}}}, 'water_chan': {'block': 0, 'buff': {'Regeneration': 5}, 'damage': 0, 'heal': 10, 'status': 'None', 'upgrades': {'raging': {'block': 0, 'buff': 'None', 'damage': 10, 'heal': 0, 'status': {'Weakness': 2}}}}}, 'columns': 7, 'energy': 5, 'hp': 100, 'rows': 4}}, f)

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
                            yaml.dump({'moves': {'basic': {0: {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'status': 'None'}, 1: {'block': 0, 'buff': {'Armor': 10}, 'damage': 10, 'heal': 0, 'status': {'weakness': 2}}, 2: {'block': 15, 'buff': {'power': 1}, 'damage': 0, 'heal': 0, 'status': {'vulnerable': 1}}}, 'special': {'block': 0, 'buff': {'lifesteal': 2}, 'damage': 10, 'heal': 20, 'status': 'None'}}, 'hp': 60, 'name': 'Devil Chan', 'phrases': {'special': ["That's a neat little hack that I found!", "With this hack, I'll steal your health for myself.", "I hope you're prepared for this.", "You know, I'm something of a scientist myself."], 'death': {0: {'clear': False, 'delay': 0.12, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 0.5, 'shake': [3, 3], 'text': 'NOOOOOOO!!!', 'wait': 0}, 1: {'clear': True, 'delay': 0.08, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.4, 'shake': [15, 15], 'text': 'THIS IS BLASPHEMYYYYYY!!! *dies*', 'wait': 1.0}}, 'basic': {0: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [2, 2], 'text': 'FOR MY LOST LOVE!!!', 'wait': 1.0}, 1: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [2, 2], 'text': 'WORLD SHAKING EXPLOSION FIST!!!', 'wait': 1.0}, 2: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [2, 2], 'text': 'NORTH STAR SPEAR!!!', 'wait': 1.0}, 3: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [2, 2], 'text': 'MILLION SOUL BOMB!!!', 'wait': 1.0}, 4: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [2, 2], 'text': 'BURNING SUN BEAM!!!', 'wait': 1.0}, 5: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [2, 2], 'text': '.2 ELECTRON VOLTS!!!', 'wait': 1.0}}, 'intro': {0: {'clear': False, 'delay': 0.1, 'fade_in': True, 'fade_out': False, 'line': 1, 'pause': 1.0, 'shake': [0, 0], 'text': 'Angel Chan...', 'wait': 0}, 1: {'clear': True, 'delay': 0.2, 'fade_in': False, 'fade_out': True, 'line': 2, 'pause': 1.3, 'shake': [5, 0], 'text': 'I loved you!', 'wait': 0.5}, 2: {'clear': True, 'delay': 0.1, 'fade_in': True, 'fade_out': True, 'line': 1, 'pause': 1.4, 'shake': [20, 20], 'text': 'How could you do this to me!?', 'wait': 1.0}}}}, f)
                        case "ms_g":
                            yaml.dump({'hp': 100, 'name': 'Ms. G', 'phrases': {'death': ['why must you use... list comphrehension... *dies*'], 'opening': ['Hello Sean!', 'How are you doing?', "Wait, you're not Sean!"]}, 'moves': {'basic_1': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrases': ['For Sean!', "I'll only give you 100% if youâ€™re one of my favourite students."], 'status': {'Vulnerable': 1}}, 'basic_2': {'block': 0, 'buff': 'None', 'damage': 15, 'heal': 0, 'phrases': ["Don't ask me, use your brain.", 'I have WELHpon *pulls out a meter stick*'], 'status': {'Weakness': 2}}, 'basic_3': {'block': 20, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrases': ['Do it on repl.it!!!', "One of them is a woman, the other has an Indian accent if you're into it."], 'status': 'None'}, 'siberia': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrases': ['You!!! How did you escape Siberia!?'], 'status': 'None'}, 'special': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrases': ['You! Go to Siberia!', 'You deserve to go to Siberia!'], 'status': 'None'}}}, f)
                        case "mr_phone":
                            yaml.dump({'hp': 200, 'name': 'Mr. Phone', 'phrases': {'death': ['Huh.', 'Looks like you did practice perfectly.', "Welp, I'll be on my way then.", '*leaves*'], 'opening': ['Did you write your TQP?']}, 'moves': {'basic_1': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrases': ['You need to touch grass.', 'My son could beat you at this game.', 'Easy choices hard life, hard choices easy life.', "It's only awkward if you make it awkward.", 'You have to build capacity.', "You chose that? Come on, that's crazy talk!!!", "Can't you be doing more?"], 'status': {'Disappointment': 1}}, 'basic_2': {'block': 0, 'buff': 'None', 'damage': 0, 'heal': 0, 'phrases': ['Almost everything is a choice... including breathing!', 'Reflect, reflect, REFLECT HARDER!!!', 'Face the monster... ME!', 'Keep your head on a swivel!'], 'status': {'Fear': 2}}, 'special': {'block': 0, 'buff': 'None', 'damage': 999, 'heal': 0, 'phrases': ['Next time, just practice perfectly.', 'My record just increased :p'], 'status': 'None'}}}, f)
        for i in self.bosses:
            with open(os.getcwd() + "/configuration/bosses/" + i + ".yml", "r") as f:
                self.boss_confs[i] = yaml.safe_load(f)

    def load_media(self):
        # ----------------------------------------------------------------------------------------------------------------------------
        # Menu Backgrounds
        self.img_menus = self.load_images_dict(os.getcwd() + "/resources/menus", (1600, 900))
        # ----------------------------------------------------------------------------------------------------------------------------
        # Level Select Images
        self.img_boss_cards = self.load_images_resize(os.getcwd() + "/resources/menus/boss_cards", (1600, 900))
        # ----------------------------------------------------------------------------------------------------------------------------
        # Cards & Card Back for Card Game
        self.img_chans = self.load_images_dict(os.getcwd() + "/resources/chan_cards/", self.chan_card_size)
        self.img_chans["card_back"] = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), self.chan_card_size)
        # ----------------------------------------------------------------------------------------------------------------------------
        # Level backgrounds
        self.img_levels = {
            1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_1/background.png").convert(), (1600, 900)),
            2: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_2/background.jpg").convert(), (1600, 900)),
            3: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_3/background.jpg").convert(), (1600, 900)),
            "siberia": pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_2/siberia.jpg").convert(), (1600, 900)),
            "Card_Game": pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_2/siberia.jpg").convert(), (1600, 900))
        }
        # ----------------------------------------------------------------------------------------------------------------------------
        # Boss Faces
        self.img_bosses = {
            1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/level_1/boss/devil_chan.png").convert_alpha(), self.boss_face_size),
            2: self.load_images_dict(os.getcwd() + "/resources/level_2/boss/", self.boss_face_size, True),
            3: self.load_images_dict(os.getcwd() + "/resources/level_3/boss/", self.boss_face_size, True)
        }
        # ----------------------------------------------------------------------------------------------------------------------------
        # Enemies
        # print(self.level_confs)
        self.img_enemies = {level: {} for level in range(1, 3)}
        self.img_enemies = self.load_images_dict(os.getcwd() + "/resources/chan_enemies/", (100, 100), True)
        # ----------------------------------------------------------------------------------------------------------------------------
        # End Screens
        self.img_end_screens = (pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/lose_screen.png").convert(), (1600, 900)),
                                pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/win_screen.png").convert(), (1600, 900)))
        # ----------------------------------------------------------------------------------------------------------------------------
        # Fonts
        self.f_hp_bar_hp = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 125)
        self.f_hp_bar_name = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 50)
        self.f_boss_text = pg.font.Font(os.getcwd() + "/resources/EXEPixelPerfect.ttf", 80)

        self.f_regular = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 50)
        self.f_regular_small = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 40)
        self.f_regular_big = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 100)

        self.f_options_title = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 75)

    def get_config(self, name):
        # print(self.player_hp, self.enable_music, self.enable_sfx, self.music_vol, self.sfx_vol,
        #       self.fps_show, self.fps_30, self.fps_60, self.fps_75, self.fps_165)
        match name:
            case "global":
                return self.global_conf
            case "level":
                return self.level_confs
            case "boss":
                return self.boss_confs

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
    def load_images_dict(path_to_directory, resize=None, alpha=False):
        """
        Args:
            path_to_directory:string:
                Directory of images
            resize:tuple:
                Size to resize images to
            alpha:boolean:
                Whether to convert the image to alpha or not
        """
        image_dict = {}
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                path = os.path.join(path_to_directory, filename)
                if resize is not None:
                    image = pg.transform.smoothscale(pg.image.load(path), resize)
                else:
                    image = pg.image.load(path)
                if alpha:
                    image_dict[(os.path.basename(filename).split(".")[0]).lower()] = image.convert_alpha()
                else:
                    image_dict[(os.path.basename(filename).split(".")[0]).lower()] = image.convert()
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
