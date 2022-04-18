import pygame as pg
import sys
import time
import os

from bin.blit_tools import draw_text_center, draw_text_left
from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *


class Options(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.background = pg.transform.scale(pg.image.load(os.getcwd() + "/resources/menus/04_settings_menu.png"),
                                             (self.width, self.height)).convert()
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
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
        self.on_buttons = []
        self.mutually_exclusives = {"FPS": []}
        self.options = None
        self.rect_dict = {"fullscreen": pg.Rect(self.align_01_x, self.align_01_y, self.button_size, self.button_size),
                          "FPS_30": pg.Rect(self.align_01_x, self.align_01_y + self.button_size * 2, self.button_size, self.button_size),
                          "FPS_60": pg.Rect(self.align_01_x, self.align_01_y + self.button_size * 4, self.button_size, self.button_size),
                          "FPS_75": pg.Rect(self.align_01_x, self.align_01_y + self.button_size * 6, self.button_size, self.button_size),
                          "FPS_165": pg.Rect(self.align_01_x, self.align_01_y + self.button_size * 8, self.button_size, self.button_size),
                          "show_FPS": pg.Rect(self.align_01_x, self.align_01_y + self.button_size * 10, self.button_size, self.button_size),
                          "null11": pg.Rect(self.align_02_x, self.align_02_y, self.button_size, self.button_size),
                          "null12": pg.Rect(self.align_02_x, self.align_02_y + self.button_size * 2, self.button_size, self.button_size),
                          "null13": pg.Rect(self.align_02_x, self.align_02_y + self.button_size * 4, self.button_size, self.button_size),
                          "null14": pg.Rect(self.align_02_x, self.align_02_y + self.button_size * 6, self.button_size, self.button_size),
                          "null15": pg.Rect(self.align_02_x, self.align_02_y + self.button_size * 8, self.button_size, self.button_size),
                          "null16": pg.Rect(self.align_02_x, self.align_02_y + self.button_size * 10, self.button_size, self.button_size),
                          "null21": pg.Rect(self.align_03_x, self.align_03_y, self.button_size, self.button_size),
                          "null22": pg.Rect(self.align_03_x, self.align_03_y + self.button_size * 2, self.button_size, self.button_size)}

    def boot(self):
        self.options = (("Video", cw_yellow, self.config.f_options_title, self.text_canvas, self.align_01_x, self.align_01_y - self.title_offset),
                        ("Fullscreen", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x + self.button_size * 2, self.align_01_y + self.text_offset),
                        ("30 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x + self.button_size * 2,
                         self.align_01_y + self.button_size * 2 + self.text_offset),
                        ("60 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x + self.button_size * 2,
                         self.align_01_y + self.button_size * 4 + self.text_offset),
                        ("75 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x + self.button_size * 2,
                         self.align_01_y + self.button_size * 6 + self.text_offset),
                        ("165 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x + self.button_size * 2,
                         self.align_01_y + self.button_size * 8 + self.text_offset),
                        ("Show FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x + self.button_size * 2,
                         self.align_01_y + self.button_size * 10 + self.text_offset),
                        ("Game Options", cw_yellow, self.config.f_options_title, self.text_canvas, self.align_02_x, self.align_02_y - self.title_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_02_x + self.button_size * 2, self.align_02_y + self.text_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_02_x + self.button_size * 2,
                         self.align_02_y + self.button_size * 2 + self.text_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_02_x + self.button_size * 2,
                         self.align_02_y + self.button_size * 4 + self.text_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_02_x + self.button_size * 2,
                         self.align_02_y + self.button_size * 6 + self.text_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_02_x + self.button_size * 2,
                         self.align_02_y + self.button_size * 8 + self.text_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_02_x + self.button_size * 2,
                         self.align_02_y + self.button_size * 10 + self.text_offset),
                        ("Music", cw_yellow, self.config.f_options_title, self.text_canvas, self.align_03_x, self.align_03_y - self.title_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_03_x + self.button_size * 2, self.align_03_y + self.text_offset),
                        ("[Placeholder]", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_03_x + self.button_size * 2,
                         self.align_03_y + self.button_size * 2 + self.text_offset))

    def draw_settings(self):
        video_header = self.config.f_options_title.render("Video", True, cw_yellow)
        # Video Settings Text Blitting
        for option in self.options:
            print(*option)
            draw_text_left(*option)
        # Button drawing
        for button in self.rect_dict:
            pg.draw.rect(self.game_canvas, light_grey, self.rect_dict[button])
        # fps_1 = pg.Rect(self.align_01_x, 300, c.square_grid, c.square_grid)
        # pg.draw.rect(self.game_canvas, white, fps_1)
        # fps_2 = pg.Rect(self.align_01_x, 400, c.square_grid, c.square_grid)
        # pg.draw.rect(self.game_canvas, white, fps_2)
        # fps_3 = pg.Rect(self.align_01_x, 500, c.square_grid, c.square_grid)
        # pg.draw.rect(self.game_canvas, white, fps_3)
        # fps_4 = pg.Rect(self.align_01_x, 600, c.square_grid, c.square_grid)
        # pg.draw.rect(self.game_canvas, white, fps_4)
        # fps_5 = pg.Rect(self.align_01_x, 700, c.square_grid, c.square_grid)
        # pg.draw.rect(self.game_canvas, white, fps_5)
        # # Applying Options
        # if fps_potato:
        #     fps_o0 = pg.Rect(100 + 5, 300 + 5, c.square_grid - 10, c.square_grid - 10)
        #     pg.draw.rect(options_menu, c.ms_red, fps_o0)
        # elif fps_30:
        #     fps_o1 = pg.Rect(100 + 5, 400 + 5, c.square_grid - 10, c.square_grid - 10)
        #     pg.draw.rect(options_menu, c.ms_red, fps_o1)
        # elif fps_60:
        #     fps_o2 = pg.Rect(100 + 5, 500 + 5, c.square_grid - 10, c.square_grid - 10)
        #     pg.draw.rect(options_menu, c.ms_red, fps_o2)
        # elif fps_75:
        #     fps_o3 = pg.Rect(100 + 5, 600 + 5, c.square_grid - 10, c.square_grid - 10)
        #     pg.draw.rect(options_menu, c.ms_red, fps_o3)
        # elif fps_165:
        #     fps_o4 = pg.Rect(100 + 5, 700 + 5, c.square_grid - 10, c.square_grid - 10)
        #     pg.draw.rect(options_menu, c.ms_red, fps_o4)
        # # FPS Mode - Text
        # fps_t1 = f_setting.render("Potato", True, white)
        # options_menu.blit(fps_t1, (200, 300))
        # fps_t2 = f_setting.render("30 FPS", True, white)
        # options_menu.blit(fps_t2, (200, 400))
        # fps_t3 = f_setting.render("60 FPS", True, white)
        # options_menu.blit(fps_t3, (200, 500))
        # fps_t4 = f_setting.render("75 FPS", True, white)
        # options_menu.blit(fps_t4, (200, 600))
        # fps_t5 = f_setting.render("165 FPS", True, white)
        # options_menu.blit(fps_t5, (200, 700))

    def collision(self, mx, my):
        for button in self.rect_dict:
            if button in self.on_buttons and self.rect_dict[button].collidepoint((mx, my)):
                self.on_buttons.remove(button)
            elif button not in self.on_buttons and self.rect_dict[button].collidepoint((mx, my)):
                self.on_buttons.append(button)

    def draw_inner_rect(self):
        for button in self.on_buttons:
            on_rect = pg.Rect(self.rect_dict[button].x + 5, self.rect_dict[button].y + 5, self.rect_dict[button].width - 10, self.rect_dict[button].height - 10)
            pg.draw.rect(self.game_canvas, red, on_rect)

    def remove_mutually_exclusive(self):
        for option in self.mutually_exclusives:
            for index, button in enumerate(self.on_buttons):
                if option in button[:len(option)] and (button, index) not in self.mutually_exclusives[option]:
                    self.mutually_exclusives[option].append((button, index))
            if len(self.mutually_exclusives[option]) > 1:
                self.on_buttons.pop(self.mutually_exclusives[option].pop(0)[1])

    def run(self):
        self.boot()
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
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.draw_settings()
            # ------------------------------------------------------------------------------------------------------------------
            if self.click:
                self.collision(mx, my)
            self.draw_inner_rect()
            self.remove_mutually_exclusive()
            print(self.on_buttons)
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
            # sound_effects_b = pg.Rect(1100, 300, c.square_grid, c.square_grid)  # SFX Button
            # pg.draw.rect(options_menu, white, sound_effects_b)
            # music_b = pg.Rect(1100, 450, c.square_grid, c.square_grid)  # Music Button
            # pg.draw.rect(options_menu, white, music_b)
            #
            # # Buttons
            # # SFX
            # if sound_effects_b.collidepoint((mx, my)):
            #     m_MS_extra_modules.draw_rect_outline(options_menu, sound_effects_b, c.ms_yellow, 5)
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
            #     sound_effects_t = f_setting.render("Sound Effects (Disabled)", True, white)
            #     options_menu.blit(sound_effects_t, (1200, 300))
            #
            # if c.music_e:
            #     music_o = pg.Rect(1100 + 5, 450 + 5, c.square_grid - 10, c.square_grid - 10)
            #     pg.draw.rect(options_menu, c.ms_red, music_o)
            #     speed_i_t = f_setting.render(f"Music ({str(int(music_volume * 100))}%)", True, white)
            #     options_menu.blit(speed_i_t, (1200, 450))
            # else:
            #     sound_effects_t = f_setting.render("Music (Disabled)", True, white)
            #     options_menu.blit(sound_effects_t, (1200, 450))
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
