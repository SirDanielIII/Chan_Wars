import sys
import time

from bin.blit_tools import draw_text_left
from bin.classes.buttons import ButtonTriangle
from bin.classes.buttons import OptionsButton
from bin.classes.health_bar import HealthBar as SoundBar
from bin.classes.level import Level
from bin.colours import *


class Options(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config, audio)
        self.audio = audio
        self.background = None
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.f_options_title = None
        self.f_regular_small = None
        # Options
        self.align_01_x = 100  # Alignment for video settings
        self.align_01_y = 275
        self.align_02_x = self.align_01_x + 350  # Alignment for game settings
        self.align_02_y = 275
        self.align_03_x = self.align_02_x + 600  # Alignment for sound settings
        self.align_03_y = 275
        self.button_size = 50
        self.title_offset = 100
        self.text_offset = 5
        self.on_buttons = ["FPS_165", "music_volume", "sfx_volume"]
        self.mutually_exclusives = {"FPS": []}
        self.rect_dict = {"FPS_30": OptionsButton(self.game_canvas, self.align_01_x, self.align_01_y, self.button_size, self.button_size, light_grey, red, orange, "FPS_30", None, cw_yellow, 10),
                          "FPS_60": OptionsButton(self.game_canvas, self.align_01_x, self.align_01_y + self.button_size * 2, self.button_size, self.button_size, light_grey, red, orange, "FPS_60", None, cw_yellow, 10),
                          "FPS_75": OptionsButton(self.game_canvas, self.align_01_x, self.align_01_y + self.button_size * 4, self.button_size, self.button_size, light_grey, red, orange, "FPS 75", None, cw_yellow, 10),
                          "FPS_165": OptionsButton(self.game_canvas, self.align_01_x, self.align_01_y + self.button_size * 6, self.button_size, self.button_size, light_grey, red, orange, "FPS 165", None, cw_yellow, 10),
                          "show_FPS": OptionsButton(self.game_canvas, self.align_02_x, self.align_02_y, self.button_size, self.button_size, light_grey, red, orange, "Show FPS", None, cw_yellow, 10),
                          "fullscreen": OptionsButton(self.game_canvas, self.align_02_x, self.align_02_y + self.button_size * 2, self.button_size, self.button_size, light_grey, red, orange, "Fullscreen", None, cw_yellow, 10),
                          "skip_intro": OptionsButton(self.game_canvas, self.align_02_x, self.align_02_y + self.button_size * 4, self.button_size, self.button_size, light_grey, red, orange, "Skip Intro", None, cw_yellow, 10),
                          "music_volume": OptionsButton(self.game_canvas, self.align_03_x, self.align_03_y, self.button_size, self.button_size, light_grey, red, orange, "Music", None, cw_yellow, 10),
                          "sfx_volume": OptionsButton(self.game_canvas, self.align_03_x, self.align_03_y + self.button_size * 4, self.button_size, self.button_size, light_grey, red, orange, "Sound Effects", None, cw_yellow, 10),}
        self.sound_sliders = {
            "music_slider_outer": pg.Rect(self.align_03_x + self.button_size * 17 / 2, self.align_03_y + self.button_size * 2, self.button_size,
                                          self.button_size),
            "sfx_slider_outer": pg.Rect(self.align_03_x + self.button_size * 17 / 2, self.align_03_y + self.button_size * 6, self.button_size,
                                        self.button_size),
            "music_slider": pg.Rect(self.align_03_x + self.button_size * 2, self.align_03_y + int(self.button_size * 2.25), self.button_size * 7,
                                    self.button_size // 2),
            "sfx_slider": pg.Rect(self.align_03_x + self.button_size * 2, self.align_03_y + int(self.button_size * 6.25), self.button_size * 7,
                                  self.button_size // 2)}
        self.music_slider_pressed = False
        self.sfx_slider_pressed = False
        self.music_bar = SoundBar(self.game_canvas, self.sound_sliders["music_slider"], 100, light_grey, white, 5)
        self.sfx_bar = SoundBar(self.game_canvas, self.sound_sliders["sfx_slider"], 100, light_grey, white, 5)

    def draw_settings(self, dt, mx, my):
        video_header = self.f_options_title.render("Video", True, cw_yellow)
        # Video Settings Text Blitting
        draw_text_left("Video", cw_yellow, self.f_options_title, self.text_canvas, self.align_01_x,
                       self.align_01_y - self.title_offset)
        # Game Settings Text Blitting
        draw_text_left("Game Options", cw_yellow, self.f_options_title, self.text_canvas, self.align_02_x,
                       self.align_02_y - self.title_offset)
        # Music Settings Text Blitting
        draw_text_left("Music", cw_yellow, self.f_options_title, self.text_canvas, self.align_03_x,
                       self.align_03_y - self.title_offset)
        # Button drawing
        self.music_bar.render(100, 0.3, dt)
        self.sfx_bar.render(100, 0.3, dt)
        pg.draw.rect(self.game_canvas, white, self.sound_sliders["music_slider_outer"])
        music_color = blue if "music_volume" in self.on_buttons else dark_grey
        pg.draw.rect(self.game_canvas, music_color,
                     [self.sound_sliders["music_slider_outer"].x + 5,
                      self.sound_sliders["music_slider_outer"].y + 5,
                      self.button_size - 10, self.button_size - 10])
        pg.draw.rect(self.game_canvas, white, self.sound_sliders["sfx_slider_outer"])
        sound_color = red if "sfx_volume" in self.on_buttons else dark_grey
        pg.draw.rect(self.game_canvas, sound_color,
                     [self.sound_sliders["sfx_slider_outer"].x + 5,
                      self.sound_sliders["sfx_slider_outer"].y + 5,
                      self.button_size - 10, self.button_size - 10])
        for button in self.rect_dict:
            self.rect_dict[button].draw_button(mx, my, button in self.on_buttons)

    def change_options(self, button, option_action):
        match button, option_action:
            case "FPS_30", "on":
                self.config.fps_value = 30
            case "FPS_60", "on":
                self.config.fps_value = 60
            case "FPS_75", "on":
                self.config.fps_value = 75
            case "FPS_165", "on":
                self.config.fps_value = 165
            case "fullscreen", "on":
                self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA and pg.FULLSCREEN)
            case "fullscreen", "off":
                self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA)
            case "show_fps", "on":
                self.config.fps_show = True
            case "show_fps", "off":
                self.config.fps_show = False
            case "music_volume", "on":
                self.audio.enable_music = True
            case "music_volume", "off":
                self.audio.enable_music = False
            case "sfx_volume", "on":
                self.audio.enable_sfx = True
            case "sfx_volume", "off":
                self.audio.enable_sfx = False

    def collision(self, mx, my):
        for button in self.rect_dict:
            option_action = None
            if button in self.on_buttons and self.rect_dict[button].check_click(mx, my, self.click):
                self.on_buttons.remove(button)
                option_action = "off"
            elif button not in self.on_buttons and self.rect_dict[button].check_click(mx, my, self.click):
                self.on_buttons.append(button)
                option_action = "on"
            self.change_options(button, option_action)

    def remove_mutually_exclusive(self):
        for option in self.mutually_exclusives:
            for button in self.on_buttons:
                if option in button[:len(option)] and button not in self.mutually_exclusives[option]:
                    self.mutually_exclusives[option].append(button)
            if len(self.mutually_exclusives[option]) > 1:
                self.on_buttons.remove(self.mutually_exclusives[option].pop(0))

    def reload(self):
        self.background = self.config.img_menus["settings"]
        self.f_options_title = self.config.f_options_title
        self.f_regular_small = self.config.f_regular_small
        for button in self.rect_dict:
            self.rect_dict[button].text_font = self.f_regular_small

    def run(self):
        self.reload()
        while 1:
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
            self.background.set_alpha(50)
            self.game_canvas.blit(self.background, (0, 0))
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.rect_dict["music_volume"].text = "Music (" + str(int(self.audio.vol_music * 100)) + "%)" if self.audio.enable_music else "Music (Disabled)"
            self.rect_dict["sfx_volume"].text = "Sound Effects (" + str(int(self.audio.vol_sfx * 100)) + "%)" if self.audio.enable_sfx else "Sound Effects (Disabled)"
            self.draw_settings(dt, mx, my)
            # ------------------------------------------------------------------------------------------------------------------
            if self.click:
                self.collision(mx, my)
            if pg.mouse.get_pressed()[0]:
                if self.sound_sliders["music_slider"].x < mx < self.sound_sliders["music_slider"].x + self.sound_sliders["music_slider"].width and "music_volume" in self.on_buttons:
                    if self.sound_sliders["music_slider_outer"].x < mx < self.sound_sliders["music_slider_outer"].x + self.button_size:
                        if self.sound_sliders["music_slider_outer"].y < my < self.sound_sliders["music_slider_outer"].y + self.button_size:
                            self.music_slider_pressed = True
                if self.sound_sliders["sfx_slider"].x < mx < self.sound_sliders["sfx_slider"].x + self.sound_sliders["sfx_slider"].width and "sfx_volume" in self.on_buttons:
                    if self.sound_sliders["sfx_slider_outer"].x < mx < self.sound_sliders["sfx_slider_outer"].x + self.button_size:
                        if self.sound_sliders["sfx_slider_outer"].y < my < self.sound_sliders["sfx_slider_outer"].y + self.button_size:
                            self.sfx_slider_pressed = True
            else:
                self.music_slider_pressed = False
                self.sfx_slider_pressed = False
            if self.music_slider_pressed:
                if self.sound_sliders["music_slider"].x < mx < self.sound_sliders["music_slider"].x + self.sound_sliders["music_slider"].width:
                    self.sound_sliders["music_slider_outer"].x = mx - self.button_size // 2
                elif self.sound_sliders["music_slider"].x > mx:
                    self.sound_sliders["music_slider_outer"].x = self.sound_sliders["music_slider"].x - self.button_size / 2
                elif self.sound_sliders["music_slider"].x + self.sound_sliders["music_slider"].width < mx:
                    self.sound_sliders["music_slider_outer"].x = self.sound_sliders["music_slider"].x + self.sound_sliders["music_slider"].width - self.button_size / 2
                self.audio.calculate_volume("music", self.sound_sliders["music_slider_outer"].x, self.sound_sliders["music_slider"].x - self.button_size / 2, self.sound_sliders["music_slider"].width)
            if self.sfx_slider_pressed:
                if self.sound_sliders["sfx_slider"].x < mx < self.sound_sliders["sfx_slider"].x + self.sound_sliders["music_slider"].width:
                    self.sound_sliders["sfx_slider_outer"].x = mx - self.button_size // 2
                elif self.sound_sliders["sfx_slider"].x > mx:
                    self.sound_sliders["sfx_slider_outer"].x = self.sound_sliders["sfx_slider"].x - self.button_size / 2
                elif self.sound_sliders["sfx_slider"].x + self.sound_sliders["sfx_slider"].width < mx:
                    self.sound_sliders["sfx_slider_outer"].x = self.sound_sliders["sfx_slider"].x + self.sound_sliders["sfx_slider"].width - self.button_size / 2
                self.audio.calculate_volume("sfx", self.sound_sliders["sfx_slider_outer"].x, self.sound_sliders["sfx_slider"].x - self.button_size / 2, self.sound_sliders["sfx_slider"].width)
            # ------------------------------------------------------------------------------------------------------------------
            self.remove_mutually_exclusive()
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                self.next_level = 2
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            self.audio.audio_mixer()
            pg.display.update()
