import sys
import time

from bin.blit_tools import display_fps
from bin.classes.buttons import ButtonTriangle, ButtonRect
from bin.classes.level import Level
from bin.colours import *


class GameMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
        self.play_button = None
        self.back_button = None
        self.left_button = None
        self.right_button = None
        self.choose_lvl = 0

    def reload(self):
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.play_button = ButtonRect(self.game_canvas, 225, 670, 350, 100, cw_blue, "FIGHT!", self.config.f_regular, white)
        self.left_button = ButtonTriangle(self.game_canvas, cw_gold, 100, 720)
        self.right_button = ButtonTriangle(self.game_canvas, cw_gold, 690, 720, "right")

    def run(self):
        self.reload()
        while 1:
            # ----------------------------------------------------------------------------------------------------------
            if not self.audio.music_channels[1].get_busy() and self.audio.enable_music:
                self.audio.dj(self.config.audio_menus["game_menu"], 1, ["music", 0], 750, True, None, None)
            # ----------------------------------------------------------------------------------------------------------
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
            self.fill_screens()
            self.game_canvas.blit(self.config.img_boss_select[self.choose_lvl], (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.choose_lvl > 0:
                if self.left_button.run(mx, my, white, self.click):
                    self.choose_lvl -= 1
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                if self.left_button.check_hover():
                    self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
                    self.next_level = 2
            if self.choose_lvl < 2:
                if self.right_button.run(mx, my, white, self.click):
                    self.choose_lvl += 1
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                if self.right_button.check_hover():
                    self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
                    self.next_level = 2
            if self.play_button.check_click(mx, my, self.click):
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 3, self.config.audio_interact["start_game"])
                self.next_level = self.choose_lvl + 11
            if self.play_button.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            self.play_button.draw_button(mx, my)
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
            if self.back_button.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
                self.next_level = 2
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.config.FPS)
            self.audio.audio_mixer()
            display_fps(self.config.fps_show, self.surface, self.clock, self.config.f_fps, self.width - 130, 15, cw_tan)
            pg.display.update()
