# Chan Wars
# By Daniel Z, Daniel F, Daniel L, and Kris

import os
import sys
import time

import pygame as pg

from bin.classes.audio import Audio
from bin.classes.config_manager import Config
from bin.levels.lvl1_devil_chan import BossDevilChan
from bin.levels.lvl3_mr_phone import BossMrPhone
from bin.levels.lvl2_boss_ms_g import BossMsG
from bin.menus.boot import Boot
from bin.menus.credits import Credits
from bin.menus.end_screen import Death
from bin.menus.game_menu import GameMenu
from bin.menus.how_to_play import HowToPlay
from bin.menus.logo import Logo
from bin.menus.main_menu import MainMenu
from bin.menus.options import Options

pg.init()
pg.mixer.pre_init(48000, -16, 2, 256)
pg.mixer.set_num_channels(24)


class Main(object):
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)
        self.game_canvas = pg.Surface((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)
        self.clock = pg.time.Clock()
        self.FPS = 165
        self.last_time = time.time()  # Used for Delta Time (Framerate Independence)
        # Pygame Window Caption
        pg.display.set_caption("Chan Wars 2: Electric Boogaloo")  # Sets Caption Text
        pg.display.set_icon(pg.image.load(os.getcwd() + "/resources/icon.png").convert_alpha())  # Caption Icon
        # Config File
        self.config = Config(self.width, self.height)
        # Audio System
        self.audio = Audio()
        # Levels
        self.lvl = 0
        self.lvl_boot = Boot(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_logo = Logo(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_main_menu = MainMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_game_menu = GameMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_options = Options(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_how_to_play = HowToPlay(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_credits = Credits(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_devil_chan = BossDevilChan(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_ms_g = BossMsG(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.lvl_mr_phone = BossMrPhone(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        self.end_screen = Death(self.width, self.height, self.surface, self.game_canvas, self.clock, self.last_time, self.config, self.audio)
        # ------------------------------------------------------------------------------------------------------------------

    def reload(self):
        pass

    def handler(self):
        while 1:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
            self.surface.fill((255, 255, 0, 0))
            # ----------------------------------------------------------------------------------------------------------
            match self.lvl:
                case 0:  # Boot Screen
                    self.lvl = self.lvl_boot.run()
                case 1:  # Dev Logo
                    self.lvl = self.lvl_logo.run()
                case 2:  # Main Menu
                    self.lvl = self.lvl_main_menu.run()
                case 3:  # Game Menu
                    self.lvl = self.lvl_game_menu.run()
                case 4:  # Options
                    self.lvl = self.lvl_options.run()
                case 5:  # How to Play
                    self.lvl = self.lvl_how_to_play.run()
                case 6:  # Credits
                    self.lvl = self.lvl_credits.run()
                case 7:  # Quit
                    pg.quit()
                    sys.exit()
                case 8:  # Lose Game State
                    self.audio.dj(None, None, None, 800, False, 10, self.config.audio_completion["lose"])
                    self.end_screen.set_background(8 - self.lvl)
                    self.lvl = self.end_screen.run()
                case 9:  # Win Game State
                    self.audio.dj(None, None, None, 800, False, 10, self.config.audio_completion["win"])
                    self.end_screen.set_background(8 - self.lvl)
                    self.lvl = self.end_screen.run()
                case 10:  # Game Over
                    pg.quit()
                case 11:  # Devil Chan Boss
                    self.lvl = self.lvl_devil_chan.run()
                case 12:  # Ms.G Boss
                    self.lvl = self.lvl_ms_g.run()
                case 13:  # Mr. Phone Boss
                    self.lvl = self.lvl_mr_phone.run()
            # ----------------------------------------------------------------------------------------------------------
            pg.display.update()
            self.clock.tick(self.FPS)


# ----------------------------------------------------------------------------------------------------------------------
main = Main()
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main.handler()

