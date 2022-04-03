import sys
import time
import os
from math import ceil

from bin.blit_tools import *
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.colours import *


class BossMsG(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.background = pg.image.load(os.getcwd() + "\\resources\\Testing_Resources\\ui_demo.png").convert()
        self.face = pg.transform.smoothscale(pg.image.load(os.getcwd() + "\\resources\\boss_02-ms_g\\ms_g_siberia-02.png").convert_alpha(), (500, 500))
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.hp_player = None
        self.hp_bar_player = None
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_boss = None
        self.hp_bar_boss = None

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        self.hp_player = self.config.player_hp
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.hp_player, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.hp_boss = self.config.get_config()["bosses"]["MsG"]["hp"]
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.hp_boss, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)

    def draw_bars(self, dt):  # Draw Health bars
        # Player Text & Health Bar
        draw_text_left(str(ceil(self.hp_player)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y + self.hp_bar_player.h * 2 + 5)
        self.hp_bar_player.render(self.hp_player, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        draw_text_right(str(ceil(self.hp_boss)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
        draw_text_right("Ms. G", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 5)
        self.hp_bar_boss.render(self.hp_boss, 0.3, dt, True)

    def run(self):
        self.reload()
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
                self.hp_boss -= random.randint(1, 12)
            # ------------------------------------------------------------------------------------------------------------------
            self.draw_bars(dt)  # Draw Health Bars (See Method Above)
            # ------------------------------------------------------------------------------------------------------------------
            # Textbox
            pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
            draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
