import sys
import time
import os

from bin.classes.buttons import BackButton
from bin.classes.level import Level
import bin.classes.load as load
from bin.classes.card_pair import MatchingScreen
from bin.colours import *


class GameMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = BackButton(self.text_canvas, cw_blue)
        self.background = pg.image.load(os.getcwd() + "/resources/Testing_Resources/level select ui demo.png").convert()

    def run(self):
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
                    if event.button == 1:  # Left Mouse Button
                        self.click = True
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            self.fill_screens()
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.game_canvas.blit(self.background, (0, 0))
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()

# Start Game Code
# size = (80, 120)
# margins = (20, 30)
# image_list = load.Load.load_images_resize(os.getcwd() + "/resources/chans", size) + \
#              [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back_PNG.png"), size)]
# background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/menus/background.jpg"), (self.width, self.height))
# f = MatchingScreen(1, image_list, self.surface)
# level = 1
#
# self.click = f.run(level, self.width, self.height, size, margins, 2 + level, (750, 500), background)[1]
# if self.click:
#     return 1
