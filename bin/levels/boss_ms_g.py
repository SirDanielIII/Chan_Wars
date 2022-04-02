import sys
import time
import os
from math import ceil

from bin.blit_tools import *
from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *


class BossMsG(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.background = pg.image.load(os.getcwd() + "\\resources\\Testing_Resources\\ui_demo.png").convert()
        self.face = pg.transform.smoothscale(pg.image.load(os.getcwd() + "\\resources\\boss_02-ms_g\\ms_g_siberia-02.png").convert_alpha(), (500, 500))
        # ------------------------------------------------------------------------------------------------------------------
        self.hp_bar_player = [100, 545, 330, 35]  # [x, y, width, height]
        self.hp_player_max = 50
        self.hp_player = self.hp_player_max
        self.hp_player_last = self.hp_player_max
        # ------------------------------------------------------------------------------------------------------------------
        self.hp_bar_boss = [1170, 545, 330, 35]
        self.hp_bar_boss_x = 330
        self.hp_bar_boss_y = 35
        self.hp_boss = None

    def run(self):
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics | Frametime
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
            self.game_canvas.fill(black)
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.click:
                self.hp_player -= random.randint(1, 12)

            if self.hp_player_last > self.hp_player:
                self.hp_player_last -= 0.2 * dt
            elif self.hp_player_last < self.hp_player:
                self.hp_player_last = self.hp_player
            print(self.hp_player_last)

            self.draw_bars()
            # ------------------------------------------------------------------------------------------------------------------
            # Textbox
            pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
            draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
            # ------------------------------------------------------------------------------------------------------------------
            # pg.draw.line(self.game_canvas, red, (95, 0), (95, 1000))
            # pg.draw.line(self.game_canvas, red, (1505, 0), (1505, 1000))
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            # print(mx, my, self.hp_player, self.hp_boss)

    def draw_bars(self):
        # Bars
        self.draw_bar_value_left(self.game_canvas, self.hp_player_max, self.hp_player, self.hp_bar_player, cw_green, white, 5, True, cw_dark_red, True, self.hp_player_last)
        # self.draw_bar_right(self.game_canvas, self.hp_bar_boss, self.hp_bar_boss_x, self.hp_bar_boss_y, cw_green, white, 5, True)
        # Player Text
        draw_text_left("You", white, self.f_name, self.text_canvas, self.hp_bar_player[0], self.hp_bar_player[1] + self.hp_bar_player[3] * 2 + 5)
        draw_text_left(str(ceil(self.hp_player)) + "HP", white, self.f_hp, self.text_canvas, self.hp_bar_player[0], self.hp_bar_player[1])
        # Boss Text
        # draw_text_right("Ms. G", white, self.f_name, self.text_canvas, self.hp_bar_boss[0] + self.hp_bar_boss[2] + 5, self.hp_bar_boss[1] + self.hp_bar_boss[3] * 2 + 5)
        # draw_text_right(str(ceil(self.hp_boss)) + "HP", white, self.f_hp, self.text_canvas, self.hp_bar_boss[0] + self.hp_bar_boss[2] + 10, self.hp_bar_boss[1])
