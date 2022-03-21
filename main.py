# Chan Wars
# By Daniel Z, Daniel F, Daniel L, and Kris

import sys
import time

import pygame as pg

from bin.classes.audio import Audio
from bin.levels.main_menu import MainMenu
from bin.levels.matching_game import Game

pg.init()
pg.mixer.pre_init(48000, -16, 2, 256)
pg.mixer.set_num_channels(16)


class Main(object):
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA and pg.FULLSCREEN)
        self.game_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA)
        self.clock = pg.time.Clock()
        self.FPS = 165
        self.last_time = time.time()  # Used for Delta Time (Framerate Independence)
        # Pygame Window Caption
        pg.display.set_caption("Chan Wars")  # Sets Caption Text
        # pg.display.set_icon(pg.image.load(os.getcwd() + "/resources/glitch/vhs_glitch_00021.png").convert_alpha())  # Caption Icon
        # Audio System
        self.audio = Audio()
        self.lvl_main_menu = MainMenu(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time)
        self.lvl_matching_game = Game(self.width, self.height, self.surface, self.game_canvas, self.clock, self.FPS, self.last_time)
        self.lvl_settings = None
        self.lvl_pause = None
        self.lvl_credits = None
        self.lvl_how_to_play = None
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
            # self.config = j.read_json("config.json")  # Update Config File
            # self.last_phase = self.config.get("phase", "")
            # ----------------------------------------------------------------------------------------------------------
            match self.lvl:
                case 0:  # Boot Screen
                    self.lvl = 1
                case 1:  # Main Menu
                    self.lvl = self.lvl_main_menu.run()
                case 2:  # Game
                    self.lvl = self.lvl_matching_game.run()
                case 3:  # Options
                    pass
                case 4:  # How to Play
                    pass
                case 5:  # Credits
                    pass
                case 6:  # Quit
                    pg.quit()
                    sys.exit()
                case 7:  # Game Screen
                    pass
            # ----------------------------------------------------------------------------------------------------------
            pg.display.update()
            self.clock.tick(self.FPS)


# ----------------------------------------------------------------------------------------------------------------------
main = Main()
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main.handler()
# Test