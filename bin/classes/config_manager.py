import yaml  # https://zetcode.com/python/yaml/
import os
import pygame as pg


# Note: [DEVIL CHAN ONLY] The values in Special Attack goes like [Attack Type, Damage, Heal]

class Config(object):
    def __init__(self):
        # Images
        self.menu_img = None
        self.boss_card = None
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
        self.default = {'bosses': {'DevilChan': {'basic': ['devilish_stab', 10], 'columns': 4, 'energy': 3, 'hp': 50, 'name': 'Devil Chan',
                                                 'phrases': {'attack': ['For My Lost Love!', 'World Shaking Explosion Fist!', 'North Star Spear!',
                                                                        'Million Soul Bomb!', 'Burning Sun Beam!', 'Point Two Electron Volts!'],
                                                             'death': ['NOOOOOOO!!!', 'THIS IS BLASPHEMYYYYYY!!! *dies*'],
                                                             'opening': ['Angel Chan... I loved you!', 'How could you do this!?'],
                                                             'special': ["That's a neat little hack that I found.",
                                                                         "With this hack, I'll steal your health for myself.",
                                                                         "I hope you're prepared for this.",
                                                                         "You know, I'm something of a scientist myself."]}, 'rows': 3,
                                                 'special': ['neat_hack', 10, 10]},
                                   'MrPhone': {'basic': ['disappointment', 0], 'columns': 4, 'energy': 5, 'hp': 200,
                                               'kill': ['thinking_question', 9999], 'name': 'Mr. Phone', 'phrases': {
                                           'attack': ['You need to touch grass.', 'My son could beat you at this game.',
                                                      'Easy choices hard life, hard choices easy life.', "It's only awkward if you make it awkward.",
                                                      'You have to build capacity.', "You chose that? Come on, that's crazy talk!!!"],
                                           'death': ['Huh.', 'Looks like you did practice perfectly.', "Welp, I'll be on my way then.", '*leaves*'],
                                           'kill': ['Next time, just practice perfectly.', 'My record just increased :p'],
                                           'opening': ['Did you write your TQP?'],
                                           'special': ['Almost everything is a choice... including breathing!', 'Reflect, reflect, REFLECT HARDER!!!',
                                                       'Face the monster... ME!', 'Keep your head on a swivel!']}, 'rows': 7,
                                               'special': ['emotional_damage', 0]},
                                   'MsG': {'basic': ['roast', 15], 'columns': 4, 'energy': 4, 'hp': 100, 'name': 'Ms. G', 'phrases': {
                                       'attack': ['For Sean!', "One of them is a woman, the other has an Indian accent if you're into it.",
                                                  "I'll only give you 100% if youâ€™re one of my favourite students.", 'Do it on Repl.it!!!',
                                                  "Don't ask me, use your brain.", 'I have WELHpon *pulls out a meter stick*'],
                                       'death': ['why must you use... list comphrehension... *dies*'],
                                       'opening': ['Hello Sean!', 'How are you doing?', "Wait, you're not Sean!"],
                                       'special': ['You! Go to Siberia!', 'You deserve to go to Siberia!']}, 'rows': 5,
                                           'special': ['siberia', 'siberia']}}, 'player': {'hp': 50},
                        'settings': {'audio': {'enable_music': True, 'enable_sfx': True, 'music_vol': 1.0, 'sfx_vol': 1.0},
                                     'fps': {'show': False, 30: False, 60: False, 75: False, 165: True}, 'fullscreen': False}}

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

    def load_media(self):
        self.menu_img = self.load_images_resize(os.getcwd() + "/resources/menus", (1600, 900))
        self.boss_card = self.load_images_resize(os.getcwd() + "/resources/menus/boss_cards", (1600, 900))

    def get_config(self):
        # print(self.player_hp, self.enable_music, self.enable_sfx, self.music_vol, self.sfx_vol,
        #       self.fps_show, self.fps_30, self.fps_60, self.fps_75, self.fps_165)
        return self.data

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

# # Test
# yeet = Config()
# yeet.load_config()
# print(yeet.get_config())
# print(yeet.get_boss_info("mr_phone"))
# print(yeet.get_boss_stat("mr_phone", "hp"))
