import sys
import time
import os
import math

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
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()

    def run(self):
        configuration = self.config.get_config()["bosses"]
        size = (120, 180)
        margins = (20, 30)
        image_list = load.Config.load_images_resize(os.getcwd() + "/resources/chans", size) + [pg.transform.scale(pg.image.load(os.getcwd() + "/resources/card_back.png"), size)]
        background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/bliss.jpg"), (self.width, self.height))
        boss_turn = True
        sprite_size = (500, 500)
        devil_chan_boss = DChan(configuration)
        player = MScreen(3, image_list, self.game_canvas)
        player_damage = 0
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ------------------------------------------------------------------------------------------------------------------
            print(boss_turn)
            if boss_turn:
                boss_state = devil_chan_boss.update(player_damage)
                devil_chan_boss.trigger_method()
                action = devil_chan_boss.act()
                action_type = action[0]
                action_quote = action[1][1]
                attack_damage = action[1][0]
                for event in pg.event.get():
                    pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                    if event.type == pg.MOUSEBUTTONDOWN:
                        mouse_pos = list(pg.mouse.get_pos())
                        boss_turn = False
            else:
                player_return = player.run(self.width, self.height, size, margins, devil_chan_boss.energy, (750, 500), background)
                boss_turn = player_return[1]
                player_damage = player_return[0]

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
