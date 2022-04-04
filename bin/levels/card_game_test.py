import random
import sys
import time
import os
import math

import bin.classes.config_manager as load
import bin.classes.stopwatch as stopwatch

from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.colours import *
from bin.classes.bosses import DevilChan as DChan
import bin.classes.card_pair as card_pair


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
        self.energy = 3
        # ------------------------------------------------------------------------------------------------------------------
        self.size = self.config.card_size
        self.margins = (20, 30)
        self.player = card_pair.MatchingScreen(0, None, self.card_canvas)
        self.pairs = None
        self.damage = 0
        self.stopwatch = stopwatch.Timer()
        # Attributes added by Daniel to make the code work. As far as I can tell, all of these are necessary

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        self.player.image_list = self.config.image_list
        self.player.columns = 3

    def run_card_game(self, click, dt):
        mouse_pos = (0, 0)
        if self.card_canvas_y != self.height:
            self.card_canvas.fill((255, 255, 255))
            # ------------------------------------------------------------------------------------------------------------------
            if not self.pairs:
                self.pairs = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
            card_complete = self.player.complete()
            if card_complete[0] == 2:
                if not self.stopwatch.activate_timer:
                    self.stopwatch.time_start()
                self.stopwatch.stopwatch()
                if self.stopwatch.seconds > 1:
                    self.damage += card_complete[2] * 10
                    self.energy -= card_complete[1]
                    self.player.reset()
                    self.stopwatch.time_reset()
            if click:
                mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_cards(mouse_pos, card_complete[0], self.config.background, 0, self.energy and not self.stopwatch.seconds > 500, self.game_canvas)
            # This is the running code made by Daniel. In order of appearance, the code generates the cards, checks to see if any pairs of choices have been made
            # starts a timer for the player to admire their choices if they have made two of them, does a bunch of stuff based on whether they chose right
            # and finally blits it all after getting the mouses position if a click has been made
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

# def run(self):
#     self.reload()
#     configuration = self.config.get_config()["bosses"]
#     size = (120, 180)
#     margins = (20, 30)
#     image_list = load.Config.load_images_resize(os.getcwd() + "/resources/chans", size) + [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), size)]
#     background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/bliss.jpg"), (self.width, self.height))
#     boss_turn = True
#     sprite_size = (250, 250)
#     boss_image = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/devil_chan.png"), sprite_size)
#     devil_chan_boss = DChan(configuration)
#     player = card_pair.MatchingScreen(3, image_list, self.card_canvas)
#     s = close_time = correct_matches = card_delay = player_damage = pairs = 0
#     f = [0]
#     energy = 3
#     delay = (750, 500)
#     mouse_pos = (0, 0)
#     while True:
#         # ------------------------------------------------------------------------------------------------------------------
#         for event in pg.event.get():
#             pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
#             if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
#                 pg.quit()
#                 sys.exit()
#             if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
#                 if event.button == 1:  # Left Mouse Button
#                     self.click = True
#                     if boss_turn:
#                         boss_turn = False
#                         s = 1
#                         close_time = 0
#                     else:
#                         mouse_pos = mx, my
#         # ------------------------------------------------------------------------------------------------------------------
#         if boss_turn:
#             boss_state = devil_chan_boss.update(player_damage)
#             energy = boss_state[1]
#             devil_chan_boss.trigger_method()
#             action = devil_chan_boss.act()
#         # ------------------------------------------------------------------------------------------------------------------
#         else:
#             if not close_time:
#                 close_time = pg.time.get_ticks()
#             if not pairs:
#                 pairs = player.generate_pairs(size, margins, ((self.width - (margins[0] + size[0]) * 3) / 2, (self.height - (margins[1] + size[1]) * 4) / 2))
#             f = player.complete()
#             if f[0] == 2:
#                 if not card_delay:
#                     card_delay = pg.time.get_ticks()
#                 if pg.time.get_ticks() > card_delay + delay[1]:
#                     correct_matches += f[2]
#                     energy -= f[1]
#                     player.reset()
#                     card_delay = 0
#                     if not energy:
#                         s = 0
#                         close_time = pg.time.get_ticks()
#                         boss_turn = True
#         # ------------------------------------------------------------------------------------------------------------------
#         self.game_canvas.fill((255, 255, 0))
#         boss_pos_mod = 15 * math.sin(pg.time.get_ticks() / 1000)
#         card_pos_mod = card_pair.move_screen(s, close_time, pg.time.get_ticks(), self.height)
#         self.game_canvas.blit(boss_image, (self.width // 2 - sprite_size[0] // 2, self.height // 2 - sprite_size[1] // 2 + boss_pos_mod))
#         player.draw_cards(mouse_pos, f[0], background, card_pos_mod, energy and not close_time + delay[0] > pg.time.get_ticks(), self.game_canvas)
#         mouse_pos = (0, 0)
