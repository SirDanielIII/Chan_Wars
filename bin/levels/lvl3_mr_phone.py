import math
import sys
import time

import bin.levels.minigames.card_game.player as card_pair
from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.entities.bosses import MrPhone
from bin.classes.entities.shopkeeper import ShopKeep
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.classes.stopwatch import Timer
from bin.colours import *


class BossMrPhone(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = self.height
        self.card_game = False
        self.game_transition_in = False
        self.game_transition_out = False  # Use this to stop the game
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.hp_bar_player = None
        self.player = card_pair.Player(self.card_canvas, None)
        self.player_attack = 0
        self.player_statuses = []
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.name = "mr_phone"
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_bar_boss = None
        self.acted = True
        self.updated = True
        self.completed = True
        self.boss = MrPhone(None)
        # ------------------------------------------------------------------------------------------------------------------
        self.size = None
        self.level = None
        self.margins = (20, 30)
        self.cards = None
        self.background = None
        self.level = None
        self.timer_dict = {"action": Timer(), "card": Timer(), "dialogue": Timer(), "transition": Timer(), "death": Timer(),
                           "update_delay": Timer()}
        self.card_complete = [0]
        self.turn_counter = 0
        self.face = None
        # ------------------------------------------------------------------------------------------------------------------
        # Shop Attributes
        self.shop_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.shopkeeper = ShopKeep(self.shop_canvas)
        # Attributes added by Daniel to make the code work. As far as I can tell, all of these are necessary

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        self.level = 3
        self.player.metadata = self.config.get_config("level")[self.level]["player"]
        self.boss.metadata = self.config.get_config("boss")[self.name]
        self.size = self.config.chan_card_size
        self.turn_counter = 0
        self.boss.initialize()
        self.player.initialize(self.config.img_cards)
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.player.health, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.boss.health, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.face = self.config.img_bosses[3]["normal"]
        self.cards = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
        self.shopkeeper.initialize(self.config.get_config("level")[self.level]["player"]["cards"], self.player.deck, self.config.img_cards)
        self.shopkeeper.create_stock()

    def draw_bars(self, dt):  # Draw Health bars
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.player.health)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y + self.hp_bar_player.h * 2 + 5)
        self.hp_bar_player.render(self.player.health, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        draw_text_right(str(math.ceil(self.boss.health)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
        draw_text_right(self.boss.metadata["name"], white, self.config.f_hp_bar_name, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 5)
        self.hp_bar_boss.render(self.boss.health, 0.3, dt, True)

    def draw_boss(self, time_elapsed):
        offset = 10 * math.sin(pg.time.get_ticks() / 500)  # VELOCITY FUNCTION HERE (SLOPE)
        center_blit_image(self.game_canvas, self.face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click):
        mouse_pos = (0, 0)
        if self.card_canvas_y != self.height:
            self.card_canvas.fill((255, 255, 255))
            # ------------------------------------------------------------------------------------------------------------------
            if self.player.energy and not self.game_transition_in and not self.game_transition_out:
                # This if statement prevents you from changing the state of the cards while the screen is moving or you don't have enough energy - Daniel
                if not self.player.cards:
                    self.player.played_cards = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
                if self.card_complete[0] != 2:
                    self.card_complete = self.player.complete()
                if self.card_complete[0] == 2:
                    if not self.timer_dict["card"].activate_timer:
                        self.timer_dict["card"].time_start()
                    if self.timer_dict["card"].seconds > 0.25:
                        print(self.card_complete, "bur")
                        self.player.energy -= 1
                        self.player_attack += self.card_complete[1]
                        self.player_statuses.append(self.card_complete[2])
                        self.player.reset()
                        self.timer_dict["card"].time_reset()
                        self.card_complete = self.player.complete()
                        print(self.player_attack, self.player_statuses, "hey")
                if click:
                    mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_cards(mouse_pos, self.card_complete[0], self.config.img_levels["Card_Game"], 0,
                                   self.player.energy and not self.timer_dict["card"].seconds > 500 and not self.game_transition_in and not self.game_transition_out)
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
        milliseconds = pg.USEREVENT
        time_elapsed = Timer()
        time_elapsed.time_start()
        pg.time.set_timer(milliseconds, 10)
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
                    for timer in self.timer_dict:  # Loop through timers and run them
                        self.timer_dict[timer].stopwatch()  # If `self.activate_timer = False` then this won't update
                    time_elapsed.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            self.game_canvas.blit(self.config.img_levels[3], (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 2
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.click and self.boss.health and self.player.health:
                if not self.card_game and self.completed and not self.game_transition_in and not self.game_transition_out:
                    # Daniel made it so that clicking won't interrupt the transitioning process
                    self.game_transition_in = True
                    self.game_transition_out = False
                elif self.card_game and self.player.energy == 0 and not self.game_transition_in and not self.game_transition_out:
                    # There should probably be a unified transitioning variable to shorten these if statements and the one above in run_card_game
                    self.game_transition_in = False
                    self.game_transition_out = True
            # Added energy and damage counter reset and only pulls down the card screen when energy is equal to 0
            # ------------------------------------------------------------------------------------------------------------------
            # Card Game Display Driver
            # Transition In
            if self.game_transition_in:
                if not self.timer_dict["transition"].activate_timer:
                    self.timer_dict["transition"].time_start()
                if self.card_canvas_y > 1:
                    self.card_canvas_y = card_pair.move_pos(True, self.timer_dict["transition"].seconds, self.height, 25)
                    # Here, Daniel rejected velocity and returned to fixed values
                elif self.card_canvas_y <= 1:
                    self.card_canvas_y = 0
                    self.game_transition_in = False
                    self.card_game = True
                    self.timer_dict["transition"].time_reset()
            # Transition Out
            if self.game_transition_out:
                if not self.timer_dict["transition"].activate_timer:
                    self.timer_dict["transition"].time_start()
                if self.card_canvas_y < self.height - 1:
                    self.card_canvas_y = card_pair.move_pos(False, self.timer_dict["transition"].seconds, self.height, 25)
                    # Here, Daniel rejected velocity and returned to fixed values
                    self.card_game = False
                elif self.card_canvas_y >= self.height - 1:
                    self.card_canvas_y = self.height
                    self.game_transition_out = False
                    self.acted = False
                    self.completed = False
                    self.updated = False
                    self.timer_dict["transition"].time_reset()
            # The stopwatch was used to do the transitions
            # I chose to just use fixed values because the impact of the framerate is practically negligible and it is so much easier to code with just the fixed values
            # Taking the derivative of the function is already a nightmare, let alone trying to implement it into the game.
            # ------------------------------------------------------------------------------------------------------------------
            if not self.card_game:  # Don't render if the card game is fully up
                if not self.timer_dict["update_delay"].activate_timer and not self.updated and not self.completed:
                    self.timer_dict["update_delay"].time_start()
                if not self.timer_dict["action"].activate_timer and not self.completed:
                    self.timer_dict["action"].time_start()
                if self.timer_dict["update_delay"].seconds > 1.5:
                    self.boss.update(self.player.attack["damage"], self.player.attack["status"])
                    if self.player.attack["damage"]:
                        self.face = self.config.img_bosses[3]["hit"]
                    self.player.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}}
                    self.updated = True
                    self.timer_dict["update_delay"].time_reset()
                if self.timer_dict["action"].seconds > 2.5 and not self.acted:
                    action = self.boss.act(self.turn_counter)
                    self.face = self.config.img_bosses[3][action[0]]
                    self.acted = True
                    self.player.update(action[2], action[3])
                elif self.timer_dict["action"].seconds > 4:
                    self.turn_counter += 1
                    self.timer_dict["action"].time_reset()
                    self.face = self.config.img_bosses[3]["normal"]
                    self.completed = True
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                self.draw_boss(time_elapsed)  # Draw Boss' Image (See Method Above)
                # Textbox
                pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
            if self.player.health <= 0:
                self.timer_dict["death"].time_start()
                if self.timer_dict["death"].seconds > 1:
                    self.config.lose_screen.set_alpha((self.timer_dict["death"].seconds - 1) * 250)
                    self.game_canvas.blit(self.config.lose_screen, (0, 0))
            elif self.boss.health <= 0:
                self.timer_dict["death"].time_start()
                if self.timer_dict["death"].seconds > 1:
                    self.config.win_screen.set_alpha((self.timer_dict["death"].seconds - 1) * 250)
                    self.game_canvas.blit(self.config.win_screen, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.boss.health and self.player.health:
                self.run_card_game(self.click)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            # print(self.clock.get_fps(), self.card_game, self.card_canvas_y, self.game_transition_in, self.game_transition_out)
