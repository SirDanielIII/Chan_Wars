import sys
import time
import os

from bin.blit_tools import center_blit_image, draw_rect_outline
from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *


class BossMsG(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.background = pg.image.load(os.getcwd() + "/resources/Testing_Resources/ui_demo.png").convert()
        self.face = pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/boss_02-ms_g/ms_g_siberia-02.png").convert_alpha(), (500, 500))
        self.hp_bar_player = [100, 545, 330, 35]  # [x, y, width, height]
        self.hp_bar_player_x = 330
        self.hp_bar_player_y = 35
        self.hp_player = None
        self.hp_bar_boss = [1170, 545, 330, 35]
        self.hp_bar_boss_x = 330
        self.hp_bar_boss_y = 35
        self.hp_boss = None

    def run(self):
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
            print(mx, my, self.hp_player, self.hp_boss)
            if self.hp_bar_player_x > 10:
                self.hp_bar_player_x -= 1 * dt
                self.hp_bar_boss_x -= 1 * dt
            self.hp_player = Level.bar_percentage(self.hp_bar_player_x, self.hp_bar_player[2])
            self.hp_boss = Level.bar_percentage(self.hp_bar_boss_x, self.hp_bar_boss[2])
            # self.game_canvas.blit(self.background, (0, 0))
            # center_blit_image(self.game_canvas, self.face, self.width / 2, self.height / 2 - 100)
            # Textbox
            pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
            draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
            # Bars
            # self.hp_bar_player_x -= 1 * dt
            self.draw_bar(self.game_canvas, self.hp_bar_player, self.hp_bar_player_x, self.hp_bar_player_y, cw_green, white, 5, True)
            self.draw_bar(self.game_canvas, self.hp_bar_boss, self.hp_bar_boss_x, self.hp_bar_boss_y, cw_green, white, 5, True)
            pg.draw.line(self.game_canvas, red, (95, 0), (95, 1000))
            pg.draw.line(self.game_canvas, red, (1505, 0), (1505, 1000))

            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
