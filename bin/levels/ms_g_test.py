import sys
import time
import os
import math

import bin.classes.config_manager as load

from bin.classes.stopwatch import Timer
from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.colours import *
from bin.classes.bosses import MsG
import bin.classes.card_pair as card_pair


class BossMsG(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = self.height
        self.card_game = False
        self.game_transition_in = False
        self.game_transition_out = False  # Use this to stop the game\
        self.energy = 4
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.hp_player = None
        self.hp_bar_player = None
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.boss_data = None
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_boss = None
        self.hp_bar_boss = None
        # ------------------------------------------------------------------------------------------------------------------
        self.size = self.config.card_size
        self.margins = (20, 30)
        self.player = card_pair.MatchingScreen(0, None, self.card_canvas)
        self.pairs = None
        self.damage = 0
        self.action_stopwatch = Timer()
        self.update_stopwatch = Timer()
        self.transition_stopwatch = Timer()
        self.turn_counter = None
        self.card_stopwatch = Timer()
        self.death_stopwatch = Timer()
        self.card_complete = [0]
        self.ms_g_boss = MsG(self.boss_data)
        self.face = None
        # Attributes added by Daniel to make the code work. As far as I can tell, all of these are necessary

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        self.player.image_list = self.config.image_list
        self.player.columns = 5
        self.boss_data = self.config.get_config()["level_2"]
        self.ms_g_boss.metadata = self.boss_data
        self.hp_player = self.boss_data["player"]["hp"]
        self.turn_counter = 0
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.hp_player, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.hp_boss = self.boss_data["boss"]["hp"]
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.hp_boss, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.face = self.config.MS_G_faces["normal"]

    def draw_bars(self, dt):  # Draw Health bars
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.hp_player)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y + self.hp_bar_player.h * 2 + 5)
        self.hp_bar_player.render(self.hp_player, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        draw_text_right(str(math.ceil(self.hp_boss)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
        draw_text_right(self.boss_data["boss"]["name"], white, self.config.f_hp_bar_name, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 5)
        self.hp_bar_boss.render(self.hp_boss, 0.3, dt, True)

    def draw_boss(self, time_elapsed):
        offset = 10 * math.sin(pg.time.get_ticks() / 500)  # VELOCITY FUNCTION HERE (SLOPE)
        center_blit_image(self.game_canvas, self.face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click):
        mouse_pos = (0, 0)
        if self.card_canvas_y != self.height:
            self.card_canvas.fill((255, 255, 255))
            # ------------------------------------------------------------------------------------------------------------------
            if self.energy and not self.game_transition_in and not self.game_transition_out:
                # This if statement prevents you from changing the state of the cards while the screen is moving or you don't have enough energy - Daniel
                if not self.pairs:
                    self.pairs = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
                self.card_complete = self.player.complete()
                if self.card_complete[0] == 2:
                    if not self.card_stopwatch.activate_timer:
                        self.card_stopwatch.time_start()
                    if self.card_stopwatch.seconds > 0.25:
                        self.damage += self.card_complete[2] * 10
                        self.energy -= self.card_complete[1]
                        self.player.reset()
                        self.card_stopwatch.time_reset()
                if click:
                    mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_cards(mouse_pos, self.card_complete[0], self.config.background, 0, self.energy and not self.card_stopwatch.seconds > 500)
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
        self.ms_g_boss.load_boss_info()
        acted = False
        completed = False
        updated = False
        milliseconds = pg.USEREVENT
        time_elapsed = Timer()
        time_elapsed.time_start()
        pg.time.set_timer(milliseconds, 10)
        self.ms_g_boss.siberia = False
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
                if event.type == milliseconds:
                    self.transition_stopwatch.stopwatch()
                    self.update_stopwatch.stopwatch()
                    self.action_stopwatch.stopwatch()
                    self.card_stopwatch.stopwatch()
                    self.death_stopwatch.stopwatch()
                    time_elapsed.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            if self.ms_g_boss.siberia:
                background = self.config.MS_G_backgrounds[1]
            else:
                background = self.config.MS_G_backgrounds[0]
            self.game_canvas.blit(background, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 2
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.click and self.hp_boss and self.hp_player:
                if not self.card_game and completed and not self.game_transition_in and not self.game_transition_out:
                    # Daniel made it so that clicking won't interrupt the transitioning process
                    self.game_transition_in = True
                    self.game_transition_out = False
                elif self.card_game and self.energy == 0 and not self.game_transition_in and not self.game_transition_out:
                    # There should probably be a unified transitioning variable to shorten these if statements and the one above in run_card_game
                    self.game_transition_in = False
                    self.game_transition_out = True
            # Added energy and damage counter reset and only pulls down the card screen when energy is equal to 0
            # ------------------------------------------------------------------------------------------------------------------
            # Card Game Display Driver
            # Transition In
            if self.game_transition_in:
                if not self.transition_stopwatch.activate_timer:
                    self.transition_stopwatch.time_start()
                if self.card_canvas_y > 1:
                    self.card_canvas_y = card_pair.move_pos(True, self.transition_stopwatch.seconds, self.height, 25)
                    # Here, Daniel rejected velocity and returned to fixed values
                elif self.card_canvas_y <= 1:
                    self.card_canvas_y = 0
                    self.game_transition_in = False
                    self.card_game = True
                    self.transition_stopwatch.time_reset()
            # Transition Out
            if self.game_transition_out:
                if not self.transition_stopwatch.activate_timer:
                    self.transition_stopwatch.time_start()
                if self.card_canvas_y < self.height - 1:
                    self.card_canvas_y = card_pair.move_pos(False, self.transition_stopwatch.seconds, self.height, 25)
                    # Here, Daniel rejected velocity and returned to fixed values
                    self.card_game = False
                elif self.card_canvas_y >= self.height - 1:
                    self.card_canvas_y = self.height
                    self.game_transition_out = False
                    acted = False
                    completed = False
                    updated = False
                    self.transition_stopwatch.time_reset()
            # The stopwatch was used to do the transitions
            # I chose to just use fixed values because the impact of the framerate is practically negligible and it is so much easier to code with just the fixed values
            # Taking the derivative of the function is already a nightmare, let alone trying to implement it into the game.
            # ------------------------------------------------------------------------------------------------------------------
            if not self.card_game:  # Don't render if the card game is fully up
                if not self.update_stopwatch.activate_timer and not updated and not completed:
                    self.update_stopwatch.time_start()
                if not self.action_stopwatch.activate_timer and not completed:
                    self.action_stopwatch.time_start()
                if self.update_stopwatch.seconds > 1.5:
                    self.ms_g_boss.update(self.damage, None)
                    self.hp_boss = self.ms_g_boss.health
                    self.energy = self.ms_g_boss.energy
                    if self.damage:
                        self.face = self.config.MS_G_faces["hit"]
                    self.damage = 0
                    updated = True
                    self.update_stopwatch.time_reset()
                if self.action_stopwatch.seconds > 2.5 and not acted:
                    action = self.ms_g_boss.act(self.turn_counter)
                    self.face = self.config.MS_G_faces["normal"]
                    if action[0] == "special":
                        self.ms_g_boss.update(0, None)
                        self.energy = self.ms_g_boss.energy
                        if not self.turn_counter:
                            self.face = self.config.MS_G_faces["siberia-01"]
                        else:
                            self.face = self.config.MS_G_faces["siberia-02"]
                    self.hp_player -= action[2]
                    self.hp_boss = self.ms_g_boss.health
                    acted = True
                elif self.action_stopwatch.seconds > 4:
                    self.turn_counter += 1
                    self.action_stopwatch.time_reset()
                    completed = True
                    self.face = self.config.MS_G_faces["normal"]
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                self.draw_boss(time_elapsed)  # Draw Boss' Image (See Method Above)
                # Textbox
                pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
            if self.hp_player <= 0:
                self.death_stopwatch.time_start()
                if self.death_stopwatch.seconds > 1:
                    self.config.end_screens[0].set_alpha((self.death_stopwatch.seconds - 1) * 250)
                    self.game_canvas.blit(self.config.lose_screen, (0, 0))
            elif self.hp_boss <= 0:
                self.death_stopwatch.time_start()
                if self.death_stopwatch.seconds > 1:
                    self.config.emd_screens[1].set_alpha((self.death_stopwatch.seconds - 1) * 250)
                    self.game_canvas.blit(self.config.win_screen, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.hp_boss and self.hp_player:
                self.run_card_game(self.click)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            # print(self.clock.get_fps(), self.card_game, self.card_canvas_y, self.game_transition_in, self.game_transition_out)
