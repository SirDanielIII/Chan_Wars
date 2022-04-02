import sys
import time
import os
import math

from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *
from bin.classes.bosses import DevilChan as DChan
import bin.classes.card_pair as card_pair
import bin.classes.config_manager as load


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()

    def run(self):
        configuration = self.config.get_config()["bosses"]
        size = (120, 180)
        margins = (20, 30)
        image_list = load.Config.load_images_resize(os.getcwd() + "/resources/chans", size) + [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), size)]
        background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/bliss.jpg"), (self.width, self.height))
        boss_turn = True
        sprite_size = (250, 250)
        boss_image = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/boss_01-devil_chan/devil_chan.png"), sprite_size)
        devil_chan_boss = DChan(configuration)
        player = card_pair.MatchingScreen(3, image_list, self.surface)
        player_damage = 0
        offset = [(self.width - (margins[0] + size[0]) * 3) / 2, (self.height - (margins[1] + size[1]) * 4) / 2]
        word = pg.font.SysFont('Comic Sans MS', 20)
        current_time = 0
        matches = 3
        correct_matches = 0
        f = [0]
        time_start = close_time = pg.time.get_ticks()
        pairs = player.generate_pairs(size, margins, offset)
        s = 1
        delay = (750, 500)
        mouse_pos = (0, 0)
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ------------------------------------------------------------------------------------------------------------------
            if boss_turn:
                boss_state = devil_chan_boss.update(player_damage)
                matches = boss_state[1]
                devil_chan_boss.trigger_method()
                action = devil_chan_boss.act()
                action_type = action[0]
                action_quote = action[1][1]
                attack_damage = action[1][0]
                for event in pg.event.get():
                    pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                    if event.type == pg.MOUSEBUTTONDOWN:
                        boss_turn = False
            # ------------------------------------------------------------------------------------------------------------------
            else:
                player.run(self.width, self.height, size, margins, matches, delay, background)

# def run(self):
#     attack_damage = 0
#     while boss_turn:
#         mouse_pos = [0, 0]
#         for event in pg.event.get():
#             pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
#             if event.type == pg.MOUSEBUTTONDOWN:
#                 mouse_pos = list(pg.mouse.get_pos())
#                 boss_turn = False
#             if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
#                 boss_turn = False
#         boss_state = self.update(damage)
#         self.trigger_method()
#         action = self.act()
#         action_type = action[0]
#         action_quote = action[1][1]
#         attack_damage = action[1][0]
#         redraw_screen(surface, 0)
#     return attack_damage, boss_turn
            self.game_canvas.blit(boss_image, (self.width // 2 - sprite_size[0] // 2, self.height // 2 - sprite_size[1] // 2))
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
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # ------------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens(not boss_turn, self.card_canvas)
            self.clock.tick(self.FPS)
            pg.display.update()
