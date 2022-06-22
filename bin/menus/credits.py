import sys
import time

from bin.blit_tools import display_fps
from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *


class Credits(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
        self.background = None
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)

    def reload(self):
        self.background = self.config.img_menus["credits"]

    def run(self):
        self.reload()
        while 1:
            # ------------------------------------------------------------------------------------------------------------------
            if not self.audio.music_channels[0].get_busy() and self.audio.enable_music:
                self.audio.dj(self.config.audio_menus["main_theme"], 0, ["music", 1], 750, True, None, None)
            # ------------------------------------------------------------------------------------------------------------------
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
            self.game_canvas.blit(self.background, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
                self.next_level = 2
            if self.back_button.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
                self.next_level = 2
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.config.FPS)
            self.audio.audio_mixer()
            display_fps(self.config.fps_show, self.surface, self.clock, self.config.f_fps, self.width - 130, 15, cw_tan)
            pg.display.update()
