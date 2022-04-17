import random
import sys
import time
import os
import math

from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.classes.stopwatch import Timer
from bin.classes.typewriter import Typewriter
from bin.colours import *
from bin.classes.card_pair import move_pos
from bin.classes.bosses import DevilChan as DChan
import bin.classes.card_pair as card_pair
import bin.classes.config_manager as load


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = self.height
        self.card_game = False
        self.game_transition_in = False
        self.game_transition_out = False
        self.energy = None
        self.size = self.config.card_size
        self.margins = (20, 30)
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.hp_player = None
        self.damage = 0
        self.hp_bar_player = None
        self.card_complete = [0]
        self.pairs = None
        self.player = card_pair.MatchingScreen(0, None, self.card_canvas)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.boss = None
        self.boss_data = None
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_boss = None
        self.hp_bar_boss = None
        # ------------------------------------------------------------------------------------------------------------------
        # Cinematic Attributes
        self.cinematic = True
        self.cinematic_line = 0
        self.typewriter = Typewriter()
        # ------------------------------------------------------------------------------------------------------------------
        # Timer Attributes
        self.timer_dict = {"action": Timer(), "card": Timer(), "death": Timer()}
        self.cinematic_timer = Timer()
        self.game_transition_time = Timer()

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes Initialization
        self.boss_data = self.config.get_config()["bosses"]["DevilChan"]
        self.boss = DChan(self.boss_data)
        self.boss.load_boss_info()
        self.hp_boss = self.boss_data["hp"]
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.hp_boss, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.boss.metadata = self.boss_data
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes Initialization
        self.hp_player = self.config.player_hp
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.hp_player, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.player.image_list = self.config.image_list
        self.player.columns = self.boss_data["columns"]
        self.energy = self.boss_data["energy"]

    def draw_bars(self, dt):  # Draw Health bars
        # ------------------------------------------------------------------------------------------------------------------
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.hp_player)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                       self.hp_bar_player.x, self.hp_bar_player.y - self.hp_bar_player.h * 3)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_player.x,
                       self.hp_bar_player.y + self.hp_bar_player.h + 5)
        self.hp_bar_player.render(self.hp_player, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        draw_text_right(str(math.ceil(self.hp_boss)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
        draw_text_right(self.boss_data["name"], white, self.config.f_hp_bar_name, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 10)
        self.hp_bar_boss.render(self.hp_boss, 0.3, dt, True)

    def draw_boss(self, dt):
        offset = 10 * math.sin(pg.time.get_ticks() / 500)
        center_blit_image(self.game_canvas, self.config.DEVIL_CHAN_face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click, dt):
        mouse_pos = (0, 0)
        if self.card_canvas_y != self.height:
            self.card_canvas.fill((0, 255, 255))
            if self.energy and not self.game_transition_in and not self.game_transition_out:
                if not self.pairs:
                    self.pairs = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
                self.card_complete = self.player.complete()
                if self.card_complete[0] == 2:
                    if not self.timer_dict["action"].activate_timer:
                        self.timer_dict["action"].time_start()
                    if self.timer_dict["action"].seconds > 0.25:
                        self.damage += self.card_complete[2] * 10
                        self.energy -= self.card_complete[1]
                        self.player.reset()
                        self.timer_dict["action"].time_reset()
                if click:
                    mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_cards(mouse_pos, self.card_complete[0], self.config.background, 0, self.energy and not self.timer_dict["action"].seconds > 500)
            self.game_canvas.blit(self.card_canvas, (0, self.card_canvas_y))

    def trigger_in(self):
        if not self.card_game:
            self.game_transition_in = True
            self.game_transition_out = False

    def trigger_out(self):
        if self.card_game:
            self.game_transition_in = False
            self.game_transition_out = True

    def textbox(self):
        pass

    def game_handler(self):
        if self.cinematic:
            print('working')
            if not self.cinematic_render():
                self.cinematic = False
        else:
            pass
            # Put textbox code in here

    def cinematic_render(self):
        s = self.cinematic_timer.seconds
        # E.G. [['Angel Chan...', 0.02, [0, 0]], ['I loved you!', 0.03, [5, 0]], ['How could you do this!?', 0.02, [20, 20]]]
        if s < 1.5:
            self.typewriter.queue_text(self.boss.opening_phrases[0][0])
        elif s >= 1.5:
            self.typewriter.render(self.text_canvas, self.boss.opening_phrases[0][1], self.config.f_boss_text, white, 100, 600, self.boss.opening_phrases[0][2], 0)
            print('working')
        print(self.cinematic_timer.seconds, self.typewriter.queue, self.typewriter.seconds)
        return True

    def run(self):
        # ----------------------------------------------------------------------------------------------------------
        self.reload()
        self.cinematic_timer.time_start()
        self.typewriter.time_start()
        # ----------------------------------------------------------------------------------------------------------
        # Custom Events
        milliseconds = pg.USEREVENT
        pg.time.set_timer(milliseconds, 10)
        # ----------------------------------------------------------------------------------------------------------
        # Initial parameters
        self.boss.load_boss_info()
        acted = True
        completed = True
        time_elapsed = Timer()
        time_elapsed.time_start()
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
                    self.game_transition_time.stopwatch()
                    self.cinematic_timer.stopwatch()
                    self.typewriter.stopwatch()
                    for timer in self.timer_dict:
                        self.timer_dict[timer].stopwatch()
                    time_elapsed.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            self.game_canvas.blit(self.config.DEVIL_CHAN_background, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            # Game Handler
            self.game_handler()
            if self.click and self.hp_boss and self.hp_player:
                if not self.card_game and completed and not self.game_transition_in and not self.game_transition_out:
                    self.trigger_in()
                elif self.card_game and self.energy == 0 and not self.game_transition_in and not self.game_transition_out:
                    self.trigger_out()
            # This is what I have on teh card game test file
            # ------------------------------------------------------------------------------------------------------------------
            # Card Game Display Driver
            # self.card_canvas_y has an offset of 1 in order to get it to work with the function used for the transition
            # Transition In
            if self.game_transition_in:
                if not self.game_transition_time.activate_timer:
                    self.game_transition_time.time_start()
                if self.card_canvas_y > 1:
                    self.card_canvas_y = move_pos(True, self.game_transition_time.seconds, self.height, 25)
                elif self.card_canvas_y <= 1:
                    self.card_canvas_y = 0
                    self.game_transition_in = False
                    self.card_game = True
                    self.game_transition_time.time_reset()
            # ------------------------------------------------------------------------------------------------------------------
            # Transition Out
            if self.game_transition_out:
                if not self.game_transition_time.activate_timer:
                    self.game_transition_time.time_start()
                if self.card_canvas_y < self.height - 1:
                    self.card_canvas_y = move_pos(False, self.game_transition_time.seconds, self.height, 25)
                    self.card_game = False
                elif self.card_canvas_y >= self.height - 1:
                    self.card_canvas_y = self.height
                    self.game_transition_out = False
                    acted = False
                    completed = False
                    self.game_transition_time.time_reset()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.card_game and not self.timer_dict["death"].seconds > 1:  # Don't render if the card game is fully up
                if not self.timer_dict["action"].activate_timer and not completed:
                    self.timer_dict["action"].time_start()
                if self.timer_dict["action"].seconds > 1:
                    self.boss.update(self.damage)
                    self.hp_boss = self.boss.health
                    self.energy = self.boss.energy
                    self.damage = 0
                if self.timer_dict["action"].seconds > 1.5 and not acted:
                    self.boss.trigger_method()
                    action = self.boss.act()
                    if action[0] != "die":
                        print(action[1][0])
                        self.hp_player -= action[1][0]
                    else:
                        pass
                    self.hp_boss = self.boss.health
                    acted = True
                elif self.timer_dict["action"].seconds > 2:
                    self.timer_dict["action"].time_reset()
                    completed = True
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                self.draw_boss(dt)  # Draw Boss' Image (See Method Above)
                # Textbox
                pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
                # ------------------------------------------------------------------------------------------------------------------
                if self.back_button.run(mx, my, cw_light_blue, self.click):
                    self.fade_out = True
                    self.next_level = 2
                if self.transition_out("game", self.game_canvas, dt):
                    self.restore()
                    return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.hp_player <= 0:
                self.timer_dict["death"].time_start()
                if self.timer_dict["death"].seconds > 1:
                    self.config.lose_screen.set_alpha((self.timer_dict["death"].seconds - 1) * 250)
                    self.game_canvas.blit(self.config.lose_screen, (0, 0))
            elif self.hp_boss <= 0:
                self.timer_dict["death"].time_start()
                if self.timer_dict["death"].seconds > 1:
                    self.config.win_screen.set_alpha((self.timer_dict["death"].seconds - 1) * 250)
                    self.game_canvas.blit(self.config.win_screen, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.hp_boss and self.hp_player:
                self.run_card_game(self.click, dt)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens(self.card_canvas, 0, self.card_canvas_y)
            self.clock.tick(self.FPS)
            pg.display.update()
            # print(self.clock.get_fps(), self.card_game, self.card_canvas_y, self.game_transition_in, self.game_transition_out)
