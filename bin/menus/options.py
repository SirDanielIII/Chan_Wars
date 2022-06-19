import sys
import time

from bin.blit_tools import draw_text_left
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar as SoundBar
from bin.classes.level import Level
from bin.colours import *
from bin.classes.audio import Audio
from bin.classes.buttons import OptionsButton


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
        self.align_02_x = self.align_01_x + 375  # Alignment for game settings
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
                          "music_volume": OptionsButton(self.game_canvas, self.align_03_x, self.align_03_y, self.button_size, self.button_size, light_grey, red, orange, "Music Volume", None, cw_yellow, 10),
                          "sfx_volume": OptionsButton(self.game_canvas, self.align_03_x, self.align_03_y + self.button_size * 4, self.button_size, self.button_size, light_grey, red, orange, "SFX Volume", None, cw_yellow, 10),}
        self.sound_sliders = {
            "music_slider_outer": pg.Rect(self.align_03_x + self.button_size * 8, self.align_03_y + self.button_size * 2, self.button_size,
                                          self.button_size),
            "sfx_slider_outer": pg.Rect(self.align_03_x + self.button_size * 8, self.align_03_y + self.button_size * 6, self.button_size,
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
            case "show_fps", "start":
                self.config.fps_show = True
            case "show_fps", "stop":
                self.config.fps_show = False
            case "music_volume", "start":
                self.audio.enable_music = True
            case "music_volume", "stop":
                self.audio.enable_music = False
            case "sfx_volume", "start":
                self.audio.enable_sfx = True
            case "sfx_volume", "stop":
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
            print(button, self.rect_dict[button].check_click(mx, my, self.click), self.click, mx, my, self.rect_dict[button].x, self.rect_dict[button].y)
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
        print(self.f_options_title)
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
            self.background.set_alpha(50)
            self.game_canvas.blit(self.background, (0, 0))
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
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
                self.audio.calculate_volume("music", self.sound_sliders["music_slider_outer"].x, self.sound_sliders["music_slider"].x, self.sound_sliders["music_slider"].width)
            if self.sfx_slider_pressed:
                if self.sound_sliders["sfx_slider"].x < mx < self.sound_sliders["sfx_slider"].x + self.sound_sliders["music_slider"].width:
                    self.sound_sliders["sfx_slider_outer"].x = mx - self.button_size // 2
                elif self.sound_sliders["sfx_slider"].x > mx:
                    self.sound_sliders["sfx_slider_outer"].x = self.sound_sliders["sfx_slider"].x - self.button_size / 2
                elif self.sound_sliders["sfx_slider"].x + self.sound_sliders["sfx_slider"].width < mx:
                    self.sound_sliders["sfx_slider_outer"].x = self.sound_sliders["sfx_slider"].x + self.sound_sliders["sfx_slider"].width - self.button_size / 2
                self.audio.calculate_volume("sfx", self.sound_sliders["sfx_slider_outer"].x, self.sound_sliders["sfx_slider"].x, self.sound_sliders["sfx_slider"].width)
            # ------------------------------------------------------------------------------------------------------------------
            self.remove_mutually_exclusive()
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 2
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            # # ------------------------------------------------------------------------------------------------------------------
            # # Game Settings - Rectangles
            # m_MS_extra_modules.draw_text("Game Settings", c.ms_yellow, f_sub_menu, options_menu, 588, 250)
            # speed_i = pg.Rect(450, 300, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, speed_i)
            # fruit_t = pg.Rect(450, 400, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, fruit_t)
            # wasd_c = pg.Rect(450, 500, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, wasd_c)
            # arrow_k_c = pg.Rect(450, 600, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, arrow_k_c)
            # show_fps_c = pg.Rect(450, 700, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, show_fps_c)
            # # Button Collisions
            # if speed_i.collidepoint((mx, my)):
            #     m_MS_extra_modules.draw_rect_outline(options_menu, speed_i, c.ms_yellow, 5)
            #     if click:
            #         c.speed_increase_e = not c.speed_increase_e
            #         a.dj(False, False, False, False, c.channel3, 500, False, c.channel3, a.ding)  # Ding Sound
            # elif fruit_t.collidepoint((mx, my)):
            #     m_MS_extra_modules.draw_rect_outline(options_menu, fruit_t, c.ms_yellow, 5)
            #     if click:
            #         c.fruit_timer_e = not c.fruit_timer_e
            #         a.dj(False, False, False, False, c.channel3, 500, False, c.channel3, a.ding)  # Ding Sound
            # elif wasd_c.collidepoint((mx, my)) and not c.WASD_e:
            #     m_MS_extra_modules.draw_rect_outline(options_menu, wasd_c, c.ms_yellow, 5)
            #     if click:
            #         c.WASD_e = True
            #         a.dj(False, False, False, False, c.channel3, 500, False, c.channel3, a.ding)  # Ding Sound
            # elif arrow_k_c.collidepoint((mx, my)) and c.WASD_e:
            #     m_MS_extra_modules.draw_rect_outline(options_menu, arrow_k_c, c.ms_yellow, 5)
            #     if click:
            #         c.WASD_e = False
            #         a.dj(False, False, False, False, c.channel3, 500, False, c.channel3, a.ding)  # Ding Sound
            # elif show_fps_c.collidepoint((mx, my)):
            #     m_MS_extra_modules.draw_rect_outline(options_menu, show_fps_c, c.ms_yellow, 5)
            #     if click:
            #         show_fps = not show_fps
            #         a.dj(False, False, False, False, c.channel3, 500, False, c.channel3, a.ding)  # Ding Sound
            # # Music - Rectangles
            # m_MS_extra_modules.draw_text("Music", c.ms_yellow, f_sub_menu, options_menu, 1156, 250)  # Header
            # sound_sfx_b = pg.Rect(1100, 300, c.square_grid, c.square_grid)  # SFX Button
            # pg.draw.rect(options_menu, white, sound_sfx_b)
            # music_b = pg.Rect(1100, 450, c.square_grid, c.square_grid)  # Music Button
            # pg.draw.rect(options_menu, white, music_b)
            #
            # # Buttons
            # # SFX
            # if sound_sfx_b.collidepoint((mx, my)):
            #     m_MS_extra_modules.draw_rect_outline(options_menu, sound_sfx_b, c.ms_yellow, 5)
            #     if click:
            #         c.sfx_e = not c.sfx_e
            #         a.dj(False, False, False, False, c.channel3, 500, False, c.channel3, a.ding)  # Ding Sound
            # # Music
            # elif music_b.collidepoint((mx, my)):
            #     m_MS_extra_modules.draw_rect_outline(options_menu, music_b, c.ms_yellow, 5)
            #     if click:
            #         c.music_e = not c.music_e
            #         if c.return_state == 1:
            #             if not c.rick_rolled:
            #                 a.dj(True, False, False, False, c.channel3, 0, True, c.channel3, a.ding)  # Click Sound
            #             else:
            #                 a.dj(False, False, False, False, c.channel3, 0, True, c.channel3, a.ding)  # Click Sound
            #         elif c.return_state == 7:
            #             a.dj(False, False, True, False, c.channel3, 0, True, c.channel3, a.ding)  # Click Sound
            #
            # # Applying Settings
            # if c.sfx_e:
            #     sfx_o = pg.Rect(1100 + 5, 300 + 5, c.square_grid - 10, c.square_grid - 10)
            #     pg.draw.rect(options_menu, c.ms_blue, sfx_o)
            #     speed_i_t = f_setting.render(f"Sound Effects ({str(int(sfx_volume * 100))}%)", True, white)
            #     options_menu.blit(speed_i_t, (1200, 300))
            # else:
            #     sound_sfx_t = f_setting.render("Sound Effects (Disabled)", True, white)
            #     options_menu.blit(sound_sfx_t, (1200, 300))
            #
            # if c.music_e:
            #     music_o = pg.Rect(1100 + 5, 450 + 5, c.square_grid - 10, c.square_grid - 10)
            #     pg.draw.rect(options_menu, c.ms_red, music_o)
            #     speed_i_t = f_setting.render(f"Music ({str(int(music_volume * 100))}%)", True, white)
            #     options_menu.blit(speed_i_t, (1200, 450))
            # else:
            #     sound_sfx_t = f_setting.render("Music (Disabled)", True, white)
            #     options_menu.blit(sound_sfx_t, (1200, 450))
            #
            # # Drawing Volume Bars
            # bar_length = 250
            # sfx_bar = pg.Rect(1200, 375, bar_length, c.square_grid / 2)
            # music_bar = pg.Rect(1200, 525, bar_length, c.square_grid / 2)
            # pg.draw.rect(options_menu, white, sfx_bar)
            # pg.draw.rect(options_menu, white, music_bar)
            #
            # # Music Bar Buttons
            # # SFX
            # sfx_button = pg.Rect(sfx_button_x, sfx_button_y, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, sfx_button)
            # selected_sfx_o = pg.Rect(sfx_button_x + 5, sfx_button_y + 5, c.square_grid - 10, c.square_grid - 10)
            # if c.sfx_e:
            #     pg.draw.rect(options_menu, c.ms_green, selected_sfx_o)
            # else:
            #     pg.draw.rect(options_menu, c.ms_grey1, selected_sfx_o)
            # # Music
            # music_button = pg.Rect(music_button_x, music_button_y, c.square_grid, c.square_grid)
            # pg.draw.rect(options_menu, white, music_button)
            # selected_music_o = pg.Rect(music_button_x + 5, music_button_y + 5, c.square_grid - 10, c.square_grid - 10)
            #
            # if c.music_e:
            #     pg.draw.rect(options_menu, c.ms_green, selected_music_o)
            # else:
            #     pg.draw.rect(options_menu, c.ms_grey1, selected_music_o)
            #
            # # SFX Slider Button
            # if sfx_button.collidepoint((mx, my)) and c.sfx_e and not selected_music:  # Sound Effects Button
            #     m_MS_extra_modules.draw_rect_outline(options_menu, sfx_button, c.ms_yellow, 5)
            #     # Click SFX
            #     if c.mouse_down:
            #         selected_sfx = True
            #         c.just_released = True
            #     if click:
            #         if selected_sfx:
            #             a.dj(False, False, False, False, c.channel3, 100, True, c.channel3, a.plop_1)  # Click Sound
            #
            # # Music Slider Button
            # elif music_button.collidepoint((mx, my)) and c.music_e and not selected_sfx:
            #     m_MS_extra_modules.draw_rect_outline(options_menu, music_button, c.ms_yellow, 5)
            #     if c.mouse_down:
            #         selected_music = True
            #         c.just_released = True
            #     # Click SFX
            #     if click:
            #         if selected_music:
            #             a.dj(False, False, False, False, c.channel3, 100, True, c.channel3, a.plop_1)  # Click Sound
            # # Unselect buttons when mouse button is released
            # if not c.mouse_down:
            #     if c.just_released:
            #         a.dj(False, False, False, False, c.channel3, 100, True, c.channel3, a.plop_2)  # Click Sound
            #         c.just_released = False
            #         selected_music = False
            #         selected_sfx = False
            # # Button Selection
            # # Sound Effects
            # if selected_sfx:
            #     m_MS_extra_modules.draw_rect_outline(options_menu, sfx_button, c.ms_yellow, 5)
            #     if 1200 <= mx <= 1450:
            #         sfx_button_x = mx - c.square_grid / 2
            #     elif mx <= 1200:
            #         sfx_button_x = 1175
            #     elif 1450 <= mx:
            #         sfx_button_x = 1425
            #
            # elif selected_music:
            #     m_MS_extra_modules.draw_rect_outline(options_menu, music_button, c.ms_yellow, 5)
            #     if 1200 <= mx <= 1450:
            #         music_button_x = mx - c.square_grid / 2
            #     elif mx <= 1200:
            #         music_button_x = 1175
            #     elif 1450 <= mx:
            #         music_button_x = 1425
            #
            # # Functions to Calculate Volume Based on X Button Coordinates
            # c_sfx_volume(sfx_button_x + c.square_grid / 2)  # Sends Rect Center For Volume Calculation
            # c_music_volume(music_button_x + c.square_grid / 2)  # Sends Rect Center For Volume Calculation
