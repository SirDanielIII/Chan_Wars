# Chan Wars
# By Daniel Z, Daniel F, Daniel L, and Kris

import sys
import time

import pygame as pg
import os

from bin.classes.audio import Audio
from bin.classes.config_manager import Config
from bin.levels.credits import Credits
from bin.levels.game_menu import GameMenu
from bin.levels.how_to_play import HowToPlay
from bin.levels.main_menu import MainMenu
from bin.levels.matching_game import Game
from bin.levels.options import Options

pg.init()
pg.mixer.pre_init(48000, -16, 2, 256)
pg.mixer.set_num_channels(16)


class Main(object):
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)
        self.game_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA)
        self.clock = pg.time.Clock()
        self.FPS = 165
        self.last_time = time.time()  # Used for Delta Time (Framerate Independence)
        # Pygame Window Caption
        pg.display.set_caption("Chan Wars")  # Sets Caption Text
        pg.display.set_icon(pg.image.load(os.getcwd() + "/resources/mr_phone/phone_thinking_question.png").convert_alpha())  # Caption Icon
        # Audio System
        self.audio = Audio()
        # Config File
        self.config = Config()
        # Levels
        self.lvl_main_menu = MainMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_game_menu = GameMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_matching_game = Game(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_options = Options(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_how_to_play = HowToPlay(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl_credits = Credits(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time, self.config)
        self.lvl = 0

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
                    self.lvl = 1
                case 1:  # Main Menu
                    self.lvl = self.lvl_main_menu.run()
                case 2:  # Game Menu
                    self.lvl = self.lvl_game_menu.run()
                case 3:  # Game
                    self.lvl = self.lvl_matching_game.run()
                case 4:  # Options
                    self.lvl = self.lvl_options.run()
                case 5:  # How to Play
                    self.lvl = self.lvl_how_to_play.run()
                case 6:  # Credits
                    self.lvl = self.lvl_credits.run()
                case 7:  # Quit
                    pg.quit()
                    sys.exit()
            # ----------------------------------------------------------------------------------------------------------
            pg.display.update()
            self.clock.tick(self.FPS)


# ----------------------------------------------------------------------------------------------------------------------
main = Main()
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main.handler()
