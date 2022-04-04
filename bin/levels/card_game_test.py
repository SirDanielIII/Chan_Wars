import random
import sys
import time
import os
import math

from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.colours import *
from bin.classes.bosses import DevilChan as DChan
import bin.classes.card_pair as card_pair
import bin.classes.config_manager as load


class Test(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = 0
        self.card_game = True
        self.game_transition_in = False
        self.game_transition_out = False  # Use this to stop the game\
        self.energy = 5

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        pass

    def run_card_game(self, click, dt):
        if self.card_canvas_y != self.height:
            self.card_canvas.fill((255, 255, 255))
            self.game_canvas.blit(self.card_canvas, (0, self.card_canvas_y))
            '''
            RUN THE CARD GAME CODE HERE
            WHEN YOU RUN OUT OF ENERGY, SET GAME_TRANSITION_OUT = TRUE (and get rid of the click stuff below)
            Essentially the card game is always blitting on top of game canvas. 
            Due to the nature of blit_screens(), game canvas is always being blit, which impacts performance.
            However, if we use the self.card_game boolean to stop the drawing of various UI elements in game canvas when it's true,
            that should increase the fps by a bit. Blitting transparent filled surfaces don't impact the FPS that much anyways (did test it).
            '''

    def run(self):
        self.reload()
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
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            self.game_canvas.fill((random.randint(0, 50), 0, random.randint(0, 50)))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 2
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            # Transition Out
            if self.game_transition_out:
                if self.card_canvas_y < self.height:
                    self.card_canvas_y += 2 * dt  # INSERT VELOCITY FUNCTION HERE
                    self.card_game = False
                elif self.card_canvas_y >= self.height:
                    self.card_canvas_y = self.height
                    self.game_transition_out = False
            # ------------------------------------------------------------------------------------------------------------------
            self.run_card_game(self.click, dt)
            if self.energy == 0:
                self.game_transition_out = True
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            print(self.clock.get_fps(), self.card_game, self.card_canvas_y, self.game_transition_in, self.game_transition_out)
