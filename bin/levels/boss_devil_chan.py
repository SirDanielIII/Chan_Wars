import sys
import time
import os

from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *
from bin.classes.bosses import DevilChan as DChan
from bin.classes.card_pair import MatchingScreen as MScreen
import bin.classes.config_manager as load


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)

    def run(self):
        configuration = self.config.get_config()["bosses"]
        devil_chan_boss = DChan(self.surface, configuration)
        size = (80, 120)
        margins = (20, 30)
        image_list = load.Config.load_images_resize(os.getcwd() + "/resources/chans", size) + \
                     [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), size)]
        background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/bliss.jpg"), (self.width, self.height))
        player = MScreen(3, image_list, self.surface)
        boss_turn = False
        while True:
            damage_taken = 0
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ------------------------------------------------------------------------------------------------------------------
            image = pg.image.load(r"C:\Users\massi\IdeaProjects\Chan_Wars\resources\boss_01-devil_chan\devil_chan.png")
            image = pg.transform.smoothscale(image, (500, 500)).convert_alpha()
            if boss_turn:
                devil_chan_boss.run(0, True, self.surface, image)
            else:
                player.run(self.width, self.height, size, margins, devil_chan_boss.energy, (750, 500), background)
#
# CHANGE BOSS METHODS TO INDIVIDUAL RUN METHODS
#

            # ------------------------------------------------------------------------------------------------------------------
            if not boss_turn:
                pass
            # ------------------------------------------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            self.game_canvas.fill((255, 0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # ------------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
