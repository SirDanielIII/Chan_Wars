# Chan Wars
# By Daniel Z, Daniel F, Daniel L, and Kris

import sys
import time

import pygame as pg
import os

from bin.classes.audio import Audio
from bin.classes.config_manager import Config
from bin.levels.boot import Boot
from bin.levels.ms_g_test import BossMsG
from bin.levels.card_game_test import Test
from bin.levels.credits import Credits
from bin.levels.card_game_test import Test as BossDevilChan
from bin.levels.game_menu import GameMenu
from bin.levels.how_to_play import HowToPlay
from bin.levels.main_menu import MainMenu
from bin.levels.boss_mr_phone import BossMrPhone
from bin.levels.options import Options

pg.init()
pg.mixer.pre_init(48000, -16, 2, 256)
pg.mixer.set_num_channels(16)


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
        pg.display.set_caption("Chan Wars")  # Sets Caption Text
        pg.display.set_icon(pg.image.load(os.getcwd() + "/resources/icon.png").convert_alpha())  # Caption Icon
        # Audio System
        self.audio = Audio()
        # Config File
        self.config = Config()
        # Levels
        self.lvl = 0
        self.lvl_boot = Boot(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_main_menu = MainMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_game_menu = GameMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_options = Options(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_how_to_play = HowToPlay(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_credits = Credits(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_devil_chan = Test(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_ms_g = BossMsG(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_mr_phone = BossMrPhone(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        # ------------------------------------------------------------------------------------------------------------------

    def handler(self):
        running = True
        # --------------------------------------------------------------------------------------------------------------
        while running:
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
                    print(self.config.get_config())
                case 1:  # Main Menu
                    self.lvl = self.lvl_main_menu.run()
                case 2:  # Game Menu
                    self.lvl = self.lvl_game_menu.run()
                case 3:  # Game Over
                    # self.lvl = self.lvl_matching_game.run()
                    self.lvl = 2
                case 4:  # Options
                    self.lvl = self.lvl_options.run()
                case 5:  # How to Play
                    self.lvl = self.lvl_how_to_play.run()
                case 6:  # Credits
                    self.lvl = self.lvl_credits.run()
                case 7:  # Quit
                    pg.quit()
                    sys.exit()
                case 10:  # Devil Chan Boss
                    self.lvl = self.lvl_devil_chan.run()
                case 11:  # Ms.G Boss
                    self.lvl = self.lvl_ms_g.run()
                case 12:  # Mr. Phone Boss
                    self.lvl = self.lvl_mr_phone.run()
            # ----------------------------------------------------------------------------------------------------------
            pg.display.update()
            self.clock.tick(self.FPS)


# ----------------------------------------------------------------------------------------------------------------------
main = Main()
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main.handler()
