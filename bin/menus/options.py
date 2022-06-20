import time

from bin.blit_tools import draw_text_left
from bin.classes.buttons import ButtonTriangle, SliderButton
from bin.classes.buttons import OptionsButton
from bin.classes.level import Level
from bin.colours import *


class Options(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
        self.audio = audio
        self.background = None
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.f_options_title = None
        self.f_regular_small = None
        # Options
        self.align_01_x = 100  # Alignment for Video settings
        self.align_y = 300
        self.align_02_x = self.align_01_x + 350  # Alignment for Game settings
        self.align_03_x = self.align_02_x + 600  # Alignment for Sound settings
        self.button_size = 50
        self.title_offset = 100

        self.stroke_size = 10
        self.buttons_fps = None
        self.buttons_settings = None
        self.buttons_music = None
        self.volume_sliders = None

        self.music_volume = None

    def defaults_from_conf(self):
        self.buttons_fps[self.config.FPS].clicked = True  # Load default FPS value
        self.buttons_settings["SHOW_FPS"].clicked = self.config.fps_show  # Load default FPS value
        self.buttons_settings["FULLSCREEN"].clicked = self.config.fullscreen  # Load default FPS value
        self.buttons_settings["SKIP_INTRO"].clicked = self.config.skip_intro  # Load default FPS value
        self.buttons_settings["FASTER_BOOT"].clicked = self.config.faster_boot  # Load default FPS value
        self.buttons_music["MUSIC"].clicked = self.audio.enable_music  # Load default FPS value
        self.buttons_music["SFX"].clicked = self.audio.enable_sfx  # Load default FPS value
        for i in self.buttons_music:
            self.lock_slider(not self.buttons_music[i].clicked, self.volume_sliders, i)

    def reload(self):
        self.background = self.config.img_menus["settings"]
        self.f_options_title = self.config.f_options_title
        self.f_regular_small = self.config.f_regular_small
        self.buttons_fps = {
            30: OptionsButton(self.game_canvas, self.align_01_x, self.align_y, self.button_size, self.button_size, self.stroke_size,
                              cw_tan, cw_gold, cw_dark_grey, cw_dark_green, "30 FPS", self.f_regular_small, white),
            60: OptionsButton(self.game_canvas, self.align_01_x, self.align_y + self.button_size * 2, self.button_size, self.button_size, self.stroke_size,
                              cw_tan, cw_gold, cw_dark_grey, cw_dark_green, "60 FPS", self.f_regular_small, white),
            75: OptionsButton(self.game_canvas, self.align_01_x, self.align_y + self.button_size * 4, self.button_size, self.button_size, self.stroke_size,
                              cw_tan, cw_gold, cw_dark_grey, cw_dark_green, "75 FPS", self.f_regular_small, white),
            144: OptionsButton(self.game_canvas, self.align_01_x, self.align_y + self.button_size * 6, self.button_size, self.button_size, self.stroke_size,
                               cw_tan, cw_gold, cw_dark_grey, cw_dark_green, "144 FPS", self.f_regular_small, white),
            165: OptionsButton(self.game_canvas, self.align_01_x, self.align_y + self.button_size * 8, self.button_size, self.button_size, self.stroke_size,
                               cw_tan, cw_gold, cw_dark_grey, cw_dark_green, "165 FPS", self.f_regular_small, white)
        }

        self.buttons_settings = {
            "SHOW_FPS": OptionsButton(self.game_canvas, self.align_02_x, self.align_y, self.button_size, self.button_size, self.stroke_size,
                                      cw_tan, cw_gold, cw_dark_grey, cw_red, "Show FPS", self.f_regular_small, white),
            "FULLSCREEN": OptionsButton(self.game_canvas, self.align_02_x, self.align_y + self.button_size * 2, self.button_size, self.button_size, self.stroke_size,
                                        cw_tan, cw_gold, cw_dark_grey, cw_dark_red, "Fullscreen", self.f_regular_small, white),
            "SKIP_INTRO": OptionsButton(self.game_canvas, self.align_02_x, self.align_y + self.button_size * 4, self.button_size, self.button_size, self.stroke_size,
                                        cw_tan, cw_gold, cw_dark_grey, cw_light_blue, "Skip Logo Intro", self.f_regular_small, white),
            "FASTER_BOOT": OptionsButton(self.game_canvas, self.align_02_x, self.align_y + self.button_size * 6, self.button_size, self.button_size, self.stroke_size,
                                         cw_tan, cw_gold, cw_dark_grey, cw_light_blue, "Faster Boot Up", self.f_regular_small, white)
        }

        self.buttons_music = {
            "MUSIC": OptionsButton(self.game_canvas, self.align_03_x, self.align_y, self.button_size, self.button_size, self.stroke_size,
                                   cw_tan, cw_gold, cw_dark_grey, cw_blue, "Music", self.f_regular_small, white),
            "SFX": OptionsButton(self.game_canvas, self.align_03_x, self.align_y + self.button_size * 4, self.button_size, self.button_size, self.stroke_size,
                                 cw_tan, cw_gold, cw_dark_grey, cw_blue, "SFX", self.f_regular_small, white)
        }
        self.volume_sliders = {
            "MUSIC": SliderButton(self.game_canvas, self.align_03_x + self.button_size * 8,
                                  self.align_03_x + self.button_size * 2, self.align_y + self.button_size * 1.5,
                                  self.button_size, self.button_size, self.stroke_size, white, cw_gold, cw_red, cw_grey,
                                  self.button_size / 3, white),
            "SFX": SliderButton(self.game_canvas, self.align_03_x + self.button_size * 8,
                                self.align_03_x + self.button_size * 2, self.align_y + self.button_size * 5.5,
                                self.button_size, self.button_size, self.stroke_size, white, cw_gold, cw_red, cw_grey,
                                self.button_size / 3, white)

        }

        self.defaults_from_conf()

    def draw_buttons(self, mx, my, dt):
        for i in self.buttons_fps:
            self.buttons_fps[i].draw_button(mx, my)
            if self.buttons_fps[i].check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            if self.buttons_fps[i].check_click(mx, my, self.click, True):
                match i:
                    case 30:
                        self.config.FPS = self.config.global_conf["settings"]["fps"]["value"] = i
                        self.turn_off_other_buttons(self.buttons_fps, i)
                    case 60:
                        self.config.FPS = self.config.global_conf["settings"]["fps"]["value"] = i
                        self.turn_off_other_buttons(self.buttons_fps, i)
                    case 75:
                        self.config.FPS = self.config.global_conf["settings"]["fps"]["value"] = i
                        self.turn_off_other_buttons(self.buttons_fps, i)
                    case 144:
                        self.config.FPS = self.config.global_conf["settings"]["fps"]["value"] = i
                        self.turn_off_other_buttons(self.buttons_fps, i)
                    case 165:
                        self.config.FPS = self.config.global_conf["settings"]["fps"]["value"] = i
                        self.turn_off_other_buttons(self.buttons_fps, i)
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["enable"])
        # ------------------------------------------------------------------------------------------------------------------
        for i in self.buttons_settings:
            self.buttons_settings[i].draw_button(mx, my, True)
            if self.buttons_settings[i].check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            if self.buttons_settings[i].check_click(mx, my, self.click):
                match i:
                    case "SHOW_FPS":
                        self.config.fps_show = self.config.global_conf["settings"]["fps"]["show"] = self.buttons_settings[i].clicked
                    case "FULLSCREEN":
                        self.config.fullscreen = self.config.global_conf["settings"]["fullscreen"] = self.buttons_settings[i].clicked
                        if self.config.fullscreen:
                            self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA and pg.FULLSCREEN)
                        else:
                            self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)
                    case "SKIP_INTRO":
                        self.config.skip_intro = self.config.global_conf["settings"]["skip_intro"] = self.buttons_settings[i].clicked
                    case "FASTER_BOOT":
                        self.config.faster_boot = self.config.global_conf["settings"]["faster_boot"] = self.buttons_settings[i].clicked
                if self.buttons_settings[i].clicked:
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["enable"])
                else:
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["disable"])
        # ------------------------------------------------------------------------------------------------------------------
        for i in self.buttons_music:
            self.buttons_music[i].draw_button(mx, my, True)
            if self.buttons_music[i].check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
            if self.buttons_music[i].check_click(mx, my, self.click):
                match i:
                    case "MUSIC":
                        self.audio.enable_music = self.config.global_conf["settings"]["audio"]["enable_music"] = self.buttons_music[i].clicked
                        self.lock_slider(not self.buttons_music[i].clicked, self.volume_sliders, i)
                    case "SFX":
                        self.audio.enable_sfx = self.config.global_conf["settings"]["audio"]["enable_sfx"] = self.buttons_music[i].clicked
                        self.lock_slider(not self.buttons_music[i].clicked, self.volume_sliders, i)
                if self.buttons_music[i].clicked:
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["enable"])
                elif self.audio.enable_sfx:
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["disable"])

        for i in self.volume_sliders:
            self.volume_sliders[i].draw_slider(mx, my, self.hold)

    @staticmethod
    def turn_off_other_buttons(button_dict, this):
        for i in button_dict:
            if i != this:
                button_dict[i].turn_off_button()

    @staticmethod
    def lock_slider(lock, button_dict, this):
        if lock:
            button_dict[this].lock_slider()
        else:
            button_dict[this].unlock_slider()

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
                    self.config.shutdown(self.config.global_conf)
                if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
                    if event.button == 1:  # Left Mouse Button
                        self.click = True
                        self.hold = True
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:  # Left Mouse Button
                        self.hold = False
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens(cw_dark_grey)
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            # Video Settings Text Blitting
            draw_text_left("Video", cw_yellow, self.f_options_title, self.text_canvas, self.align_01_x, self.align_y - self.title_offset)
            draw_text_left("Game Options", cw_yellow, self.f_options_title, self.text_canvas, self.align_02_x, self.align_y - self.title_offset)
            draw_text_left("Music", cw_yellow, self.f_options_title, self.text_canvas, self.align_03_x, self.align_y - self.title_offset)
            # ------------------------------------------------------------------------------------------------------------------
            self.draw_buttons(mx, my, dt)
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
                self.next_level = 2
            if self.back_button.check_hover():
                self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
                self.next_level = 2
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.config.FPS)
            self.audio.audio_mixer()
            pg.display.update()
