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
        self.image_list = None
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
        # Other
        self.highest_level_beat = None
        self.boss_face_size = None
        # ----------------------------------------------------------------------------------------------------------------------------
        self.card_size = (120, 180)
        # Settings
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
        self.default = {'bosses': {'DevilChan': {'basic': ['devilish_stab', 10], 'columns': 3, 'energy': 3, 'hp': 60, 'name': 'Devil Chan', 'phrases': {
            'attack': ['For My Lost Love!', 'World Shaking Explosion Fist!', 'North Star Spear!', 'Million Soul Bomb!', 'Burning Sun Beam!', 'Point Two Electron Volts!'],
            'death': ['NOOOOOOO!!!', 'THIS IS BLASPHEMYYYYYY!!! *dies*'],
            'opening': [['Angel Chan...', 0.1, [0, 0], 1.0], ['I loved you!', 0.3, [5, 0]], ['How could you do this!?', 0.2, [20, 20]]],
            'special': ["That's a neat little hack that I found!", "With this hack, I'll steal your health for myself.", "I hope you're prepared for this.",
                        "You know, I'm something of a scientist myself."]}, 'rows': 4, 'special': ['neat_hack', 10, 10]},
                                   'MrPhone': {'basic': ['disappointment', 0], 'columns': 7, 'energy': 4, 'hp': 200, 'kill': ['thinking_question', 9999], 'name': 'Mr. Phone',
                                               'phrases': {
                                                   'attack': ['You need to touch grass.', 'My son could beat you at this game.', 'Easy choices hard life, hard choices easy life.',
                                                              "It's only awkward if you make it awkward.", 'You have to build capacity.',
                                                              "You chose that? Come on, that's crazy talk!!!", "Can't you be doing more?"],
                                                   'death': ['Huh.', 'Looks like you did practice perfectly.', "Welp, I'll be on my way then.", '*leaves*'],
                                                   'kill': ['Next time, just practice perfectly.', 'My record just increased :p'], 'opening': ['Did you write your TQP?'],
                                                   'special': ['Almost everything is a choice... including breathing!', 'Reflect, reflect, REFLECT HARDER!!!',
                                                               'Face the monster... ME!', 'Keep your head on a swivel!']}, 'rows': 4, 'special': ['emotional_damage', 0]},
                                   'MsG': {'basic': ['roast', 15], 'columns': 4, 'energy': 4, 'hp': 100, 'name': 'Ms. G', 'phrases': {
                                       'attack': ['For Sean!', "One of them is a woman, the other has an Indian accent if you're into it.",
                                                  "I'll only give you 100% if youâ€™re one of my favourite students.", 'Do it on repl.it!!!', "Don't ask me, use your brain.",
                                                  'I have WELHpon *pulls out a meter stick*'], 'death': ['why must you use... list comphrehension... *dies*'],
                                       'opening': ['Hello Sean!', 'How are you doing?', "Wait, you're not Sean!"],
                                       'special': ['You! Go to Siberia!', 'You deserve to go to Siberia!']}, 'rows': 5, 'special': ['siberia', 'siberia']}},
                        'other': {'boss_face_size': [500, 500], 'highest_level_beat': 0}, 'player': {'hp': 50},
                        'settings': {'audio': {'enable_music': True, 'enable_sfx': True, 'music_vol': 1.0, 'sfx_vol': 1.0},
                                     'fps': {'show': False, 30: False, 60: False, 75: False, 165: True}, 'fullscreen': False}}

    def load_config(self):
        if not os.path.exists(os.getcwd() + "/config.yml"):
            with open(os.getcwd() + "/config.yml", "w") as f:
                yaml.dump(self.default, f)
                self.default = None
        with open(os.getcwd() + "/config.yml", "r") as f:
            self.data = yaml.safe_load(f)
            self.enable_music = self.data["settings"]["audio"]["enable_music"]
            self.enable_sfx = self.data["settings"]["audio"]["enable_sfx"]
            self.music_vol = self.data["settings"]["audio"]["music_vol"]
            self.sfx_vol = self.data["settings"]["audio"]["sfx_vol"]
            self.fps_show = self.data["settings"]["fps"]["show"]
            self.fps_30 = self.data["settings"]["fps"][30]
            self.fps_60 = self.data["settings"]["fps"][60]
            self.fps_75 = self.data["settings"]["fps"][75]
            self.fps_165 = self.data["settings"]["fps"][165]
            self.highest_level_beat = self.data["other"]["highest_level_beat"]
            self.boss_face_size = self.data["other"]["boss_face_size"]

    def load_media(self):
        self.menu_img = self.load_images_resize(os.getcwd() + "/resources/menus", (1600, 900))
        self.boss_card = self.load_images_resize(os.getcwd() + "/resources/menus/boss_cards", (1600, 900))
        # ----------------------------------------------------------------------------------------------------------------------------
        self.image_list = self.load_images_resize(os.getcwd() + "/resources/chans", self.card_size) + \
                          [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), self.card_size)]
        self.backgrounds = {"Card Game": pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/bliss.jpg").convert(), (1600, 900)),
                            1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/Chan_background.png").convert(), (1600, 900)),
                            2: [pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/ms_g_non-siberia_background.jpg").convert(), (1600, 900)),
                                        pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/ms_g_siberia_background.jpg").convert(), (1600, 900))],
                            3: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_03-mr_phone/mr_phone_background.jpg").convert(), (1600, 900))}
        self.end_screens = (pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/lose_screen.png").convert(), (1600, 900)),
                            pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/win_screen.png").convert(), (1600, 900)))
        self.enemies_images = {name: pg.transform.smoothscale(pg.image.load(os.getcwd() + "\\resources\\" + name + ".jpg").convert(), (100, 100)) for name in ["flying", "drowned"]} # self.data["level_1"]["enemies"]
        self.f_hp_bar_hp = pg.font.Font(os.getcwd() + "\\resources\\EXEPixelPerfect.ttf", 125)
        self.f_hp_bar_name = pg.font.Font(os.getcwd() + "\\resources\\EXEPixelPerfect.ttf", 50)
        self.f_boss_text = pg.font.Font(os.getcwd() + "\\resources\\EXEPixelPerfect.ttf", 80)
        self.f_options_title = pg.font.Font(os.getcwd() + "\\resources\\Herculanum-Regular.ttf", 75)
        self.f_options_sub = pg.font.Font(os.getcwd() + "\\resources\\Herculanum-Regular.ttf", 40)
        self.face_images = {1: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/devil_chan.png").convert_alpha(), self.boss_face_size),
                            2: {filename[5:-4]: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/" + filename), self.boss_face_size).convert_alpha()
                                for filename in os.listdir(os.getcwd() + "/resources/boss_02-ms_g/") if filename.endswith(".png")},
                            3: {filename[6:-4]: pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_03-mr_phone/" + filename), self.boss_face_size).convert_alpha()
                                for filename in os.listdir(os.getcwd() + "/resources/boss_03-mr_phone/") if filename.endswith(".png")}}

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
