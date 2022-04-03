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


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Additional Attributes
        self.size = (120, 180)
        self.sprite_size = 200, 200
        self.margins = (20, 30)
        self.image_list = load.Config.load_images_resize(os.getcwd() + "/resources/chans", self.size) + \
                          [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), self.size)]
        self.background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/bliss.jpg"), (self.width, self.height))
        self.boss_image = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/devil_chan.png"), self.sprite_size)
        self.card_delay = 0
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = self.height
        self.card_game = False
        self.game_transition_in = False
        self.game_transition_out = False
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.boss_data = None
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_boss = None
        self.hp_bar_boss = None
        self.columns = 3
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.energy = None
        self.hp_player = None
        self.hp_bar_player = None
        self.damage = 0
        self.player = card_pair.MatchingScreen(self.columns, self.image_list, self.card_canvas)
        self.pairs = self.player.generate_pairs(self.size, self.margins,
                                                ((self.width - (self.margins[0] + self.size[0]) * 3) / 2, (self.height - (self.margins[1] + self.size[1]) * 4) / 2))
        self.complete_card = [0]



    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        self.boss_data = self.config.get_config()["bosses"]["DevilChan"]
        self.energy = self.boss_data["energy"]
        self.hp_player = self.config.player_hp
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.hp_player, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.hp_boss = self.boss_data["hp"]
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.hp_boss, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)

    def draw_bars(self, dt):  # Draw Health bars
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.hp_player)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y + self.hp_bar_player.h * 2 + 5)
        self.hp_bar_player.render(self.hp_player, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        draw_text_right(str(math.ceil(self.hp_boss)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
        draw_text_right(self.boss_data["name"], white, self.config.f_hp_bar_name, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 5)
        self.hp_bar_boss.render(self.hp_boss, 0.3, dt, True)

    def draw_boss(self, dt):
        offset = 15 * math.sin(pg.time.get_ticks() / 1000)  # VELOCITY FUNCTION HERE (SLOPE)
        center_blit_image(self.game_canvas, self.config.DEVIL_CHAN_face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click, dt, delay, close_time):
        if self.card_canvas_y != self.height:
            self.card_canvas.fill((255, 255, 255))
            self.game_canvas.blit(self.card_canvas, (0, self.card_canvas_y))
            if not self.pairs:
                self.pairs = self.player.generate_pairs(self.size, self.margins,
                                                        ((self.width - (self.margins[0] + self.size[0]) * 3) / 2, (self.height - (self.margins[1] + self.size[1]) * 4) / 2))
            self.complete_card = self.player.complete()
            if self.complete_card[0] == 2:
                if not self.card_delay:
                    self.card_delay = pg.time.get_ticks()
                if pg.time.get_ticks() > self.card_delay + delay[1]:
                    self.damage += self.complete_card[2] * 10
                    self.energy -= self.complete_card[1]
                    self.player.reset()
                    self.card_delay = 0
                    if not self.energy:
                        s = 0
                        close_time = pg.time.get_ticks()
                        boss_turn = True
        return self.damage

    def run(self):
        self.reload()
        close_time = 0
        out_time = 0
        in_time = 0
        delay = 750, 500
        mouse_pos = (0, 0)
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
            self.game_canvas.fill((0, 255, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 2
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.click:
                self.hp_player -= random.randint(1, 12)
                self.hp_boss -= random.randint(1, 12)
                if not self.card_game:
                    self.game_transition_in = True
                    self.game_transition_out = False
                    in_time = pg.time.get_ticks()
                    self.card_game = True
                else:
                    self.game_transition_in = False
                    self.game_transition_out = True
                    out_time = pg.time.get_ticks()
            # ------------------------------------------------------------------------------------------------------------------
            # Card Game Display Driver
            # Transition In
            if self.game_transition_in:
                if self.card_canvas_y > 0:
                    if not in_time:
                        in_time = pg.time.get_ticks()
                    self.card_canvas_y = card_pair.move_screen(self.game_transition_in, in_time, pg.time.get_ticks(), self.height)  # INSERT VELOCITY FUNCTION HERE
                elif self.card_canvas_y <= 0:
                    self.card_canvas_y = 0
                    self.game_transition_in = False
                    self.card_game = True
            # Transition Out
            if self.game_transition_out:
                if self.card_canvas_y < self.height:
                    self.card_canvas_y -= 100 * dt  # INSERT VELOCITY FUNCTION HERE
                    self.card_game = False
                elif self.card_canvas_y >= self.height:
                    self.card_canvas_y = self.height
                    self.game_transition_out = False
            # ------------------------------------------------------------------------------------------------------------------
            if not self.card_game:  # Don't render if the card game is fully up
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                self.draw_boss(dt)  # Draw Boss' Image (See Method Above)
                # Textbox
                pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
            # ------------------------------------------------------------------------------------------------------------------
            else:
                if not close_time:
                    close_time = pg.time.get_ticks()
                thing = self.run_card_game(self.click, dt, delay, close_time)
                print(thing)
            # ------------------------------------------------------------------------------------------------------------------
            if self.click:
                mouse_pos = mx, my
            card_pos_mod = card_pair.move_screen(self.game_transition_in, close_time, pg.time.get_ticks(), self.height)
            self.player.draw_cards(mouse_pos, self.complete_card[0], self.background, card_pos_mod, self.energy and not close_time + delay[0] > pg.time.get_ticks(), self.game_canvas)
            mouse_pos = (0, 0)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens(not self.card_game, self.card_canvas)
            self.clock.tick(self.FPS)
            pg.display.update()
            # print(self.clock.get_fps(), self.card_game, self.card_canvas_y, self.game_transition_in, self.game_transition_out)

    def run_game(self):
        self.reload()
        configuration = self.config.get_config()["bosses"]
        size = (120, 180)
        margins = (20, 30)
        image_list = load.Config.load_images_resize(os.getcwd() + "/resources/chans", size) + [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), size)]
        background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/bliss.jpg"), (self.width, self.height))
        boss_turn = True
        sprite_size = (250, 250)
        boss_image = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/devil_chan.png"), sprite_size)
        devil_chan_boss = DChan(configuration)
        player = card_pair.MatchingScreen(3, image_list, self.card_canvas)
        in_out = close_time = correct_matches = card_delay = player_damage = pairs = 0
        card_complete = [0]
        energy = 3
        delay = (750, 500)
        mouse_pos = (0, 0)
        while True:
            # ------------------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
                    if event.button == 1:  # Left Mouse Button
                        self.click = True
                        if boss_turn:
                            boss_turn = False
                            in_out = 1
                            close_time = 0
                        else:
                            mouse_pos = list(pg.mouse.get_pos())
            # ------------------------------------------------------------------------------------------------------------------
            if boss_turn:
                boss_state = devil_chan_boss.update(player_damage)
                energy = boss_state[1]
                devil_chan_boss.trigger_method()
                action = devil_chan_boss.act()
            # ------------------------------------------------------------------------------------------------------------------
            else:
                if not close_time:
                    close_time = pg.time.get_ticks()
                if not pairs:
                    pairs = player.generate_pairs(size, margins, ((self.width - (margins[0] + size[0]) * 3) / 2, (self.height - (margins[1] + size[1]) * 4) / 2))
                card_complete = player.complete()
                if card_complete[0] == 2:
                    if not card_delay:
                        card_delay = pg.time.get_ticks()
                    if pg.time.get_ticks() > card_delay + delay[1]:
                        correct_matches += card_complete[2]
                        energy -= card_complete[1]
                        player.reset()
                        card_delay = 0
                        if not energy:
                            in_out = 0
                            close_time = pg.time.get_ticks()
                            boss_turn = True
            # ------------------------------------------------------------------------------------------------------------------

