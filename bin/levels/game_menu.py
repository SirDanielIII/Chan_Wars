import pygame as pg
import sys
import time
import os

from bin.classes.level import Level
import bin.classes.load as load
from bin.classes.card_pair import MatchingScreen


class GameMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)

    def run(self):
        size = (80, 120)
        margins = (20, 30)
        image_list = load.Load.load_images_resize(os.getcwd() + "/resources/chans", size) + \
                     [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back_PNG.png"), size)]
        background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/background.jpg"), (self.width, self.height))
        f = MatchingScreen(1, image_list, self.surface)
        level = 1

        self.click = f.run(level, self.width, self.height, size, margins, 2 + level, (750, 500), background)[1]
        if self.click:
            return 1
        # while True:
        #     # Framerate Independence
        #     dt = time.time() - self.last_time
        #     dt *= 60  # Delta time - 60fps physics
        #     self.last_time = time.time()
        #     self.click = False
        #     mx, my = pg.mouse.get_pos()  # Get mouse position
        #     # ----------------------------------------------------------------------------------------------------------
        #     for event in pg.event.get():
        #         pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
        #         if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
        #             pg.quit()
        #             sys.exit()
        #         if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
        #             if event.button == 1:  # Left Mouse Button
        #                 self.click = True
        #
        #     # ------------------------------------------------------------------------------------------------------------------
        #     self.fill_screens()
        #     self.surface.fill((255, 0, 0))
        #     if self.click:
        #         return 1
        #     # ------------------------------------------------------------------------------------------------------------------
        #     self.blit_screens()
        #     self.clock.tick(self.FPS)
        #
        #     pg.display.update()
