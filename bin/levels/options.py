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
        self.align_01_x = 100
        self.align_01_y = 300
        self.button_size = 50

    def draw_fps_settings(self):
        # FPS Mode - Rectangles

        video_header = self.config.f_options_title.render("Video", True, cw_yellow)
        draw_text_left("Video", cw_yellow, self.config.f_options_title, self.text_canvas, self.align_01_x, 265)
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
        draw_text_left("Fullscreen", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x, self.align_01_y)
        draw_text_left("Show FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x, self.align_01_y + self.button_size * 2)
        draw_text_left("30 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x, self.align_01_y + self.button_size * 4)
        draw_text_left("60 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x, self.align_01_y + self.button_size * 6)
        draw_text_left("75 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x, self.align_01_y + self.button_size * 8)
        draw_text_left("165 FPS", cw_yellow, self.config.f_options_sub, self.text_canvas, self.align_01_x, self.align_01_y + self.button_size * 10)
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
            self.background.set_alpha(50)
            self.game_canvas.blit(self.background, (0, 0))

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
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.draw_fps_settings()
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            print(mx, my)
