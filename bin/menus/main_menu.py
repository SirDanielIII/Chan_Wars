import sys
import time

from bin.blit_tools import display_fps
from bin.classes.buttons import ButtonRect
from bin.classes.level import Level
from bin.colours import *


class MainMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
        self.audio = audio
        self.f_regular_small = None
        self.f_regular = None
        self.f_regular_big = None
        self.background = None
        self.b_play_game = None
        self.b_options = None
        self.b_help = None
        self.b_credits = None
        self.b_quit = None
        self.buttons = None

    def reload(self):
        self.f_regular_small = self.config.f_regular_small
        self.f_regular = self.config.f_regular
        self.f_regular_big = self.config.f_regular_big
        self.background = self.config.img_menus["main"]
        # Create Button Classes
        self.b_play_game = ButtonRect(self.game_canvas, 100, 400, 650, 150, cw_dark_green, "Play Game", self.config.f_regular_big, white)
        self.b_options = ButtonRect(self.game_canvas, 100, 600, 300, 100, cw_blue, "Options", self.config.f_regular, white)
        self.b_help = ButtonRect(self.game_canvas, 450, 600, 300, 100, cw_blue, "How to Play", self.config.f_regular_small, white)
        self.b_credits = ButtonRect(self.game_canvas, 100, 750, 300, 100, cw_blue, "Credits", self.config.f_regular, white)
        self.b_quit = ButtonRect(self.game_canvas, 450, 750, 300, 100, cw_red, "Quit", self.config.f_regular, white)
        self.buttons = [self.b_play_game, self.b_options, self.b_help, self.b_credits, self.b_quit]
        self.transition_speed = 10

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
            # ------------------------------------------------------------------------------------------------------------------
            self.game_canvas.blit(self.background, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            for i in self.buttons:
                i.draw_button(mx, my)
            # --------------------------------------------------------------------------------------------------------------
            if self.b_play_game.check_click(mx, my, self.click):
                self.next_level = 3
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
            if self.b_play_game.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            # --------------------------------------------------------------------------------------------------------------
            if self.b_options.check_click(mx, my, self.click):
                self.next_level = 4
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
            if self.b_options.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            # --------------------------------------------------------------------------------------------------------------
            if self.b_help.check_click(mx, my, self.click):
                self.next_level = 5
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
            if self.b_help.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            # --------------------------------------------------------------------------------------------------------------
            if self.b_credits.check_click(mx, my, self.click):
                self.next_level = 6
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
            if self.b_credits.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            # --------------------------------------------------------------------------------------------------------------
            if self.b_quit.check_click(mx, my, self.click):
                self.next_level = 7
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
            if self.b_quit.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
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
