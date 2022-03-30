import sys
import time
import os
from pygame import gfxdraw

from bin.classes.level import Level
from bin.colours import *


class Boot(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.background = pg.image.load(os.getcwd() + "/resources/menus/boot_menu.png").convert()
        self.phase = 0
        self.alpha_game = 255
        self.fade_in = False

    def run(self):
        # ------------------------------------------------------------------------------------------------------------------
        # || WARNING ||
        # THIS IS LEGACY CODE FROM MODERN SNEK
        # Recode this section if necessary (probably not cause this game isn't very image heavy)
        # ------------------------------------------------------------------------------------------------------------------
        start_ticks = pg.time.get_ticks()
        play_sfx = 0
        rect_width = 0
        f_boot = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 75)
        boot_sound = pg.mixer.Sound(os.getcwd() + "/resources/boot/boot_bootup.mp3")
        boot_sound.set_volume(0.3)
        boot_finished = pg.mixer.Sound(os.getcwd() + "/resources/boot/boot_confirm.mp3")
        boot_finished.set_volume(0.4)
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            # ------------------------------------------------------------------------------------------------------------------
            seconds = (pg.time.get_ticks() - start_ticks) / 1000  # Timer
            pg.draw.rect(self.game_canvas, white, (150, self.height - 200, rect_width, 50))  # Loading Bar
            gfxdraw.rectangle(self.game_canvas, (140, self.height - 210, self.width - 280, 70), white)  # Bar Outline
            if rect_width < 1300 and seconds < 2.5:  # Bug Fix - Timer doesn't count when dragging window; snaps to end
                if play_sfx == 0:  # Plays the sound effect once
                    pg.mixer.Channel(0).play(boot_sound)
                    play_sfx = 1  # Change value to avoid loop
                if seconds < 0.25:
                    f_boot_render = f_boot.render("LOADING CONFIG FILE", True, white)
                    self.game_canvas.blit(f_boot_render, (140, 610))
                    rect_width += 10
                    self.config.load_config()
                elif seconds < 1:
                    f_boot_render = f_boot.render("CONFIG FILE LOADED", True, white)
                    self.game_canvas.blit(f_boot_render, (140, 610))
                    rect_width += 2
                elif seconds < 1.6:
                    loading_render = f_boot.render("Gathering the Chans", True, white)
                    self.game_canvas.blit(loading_render, (140, 610))
                    rect_width += 2
                elif seconds < 2:
                    loading_render = f_boot.render("Running Away From Mr. Phone", True, white)
                    self.game_canvas.blit(loading_render, (140, 610))
                    rect_width += 7
                elif seconds < 2.5:
                    loading_render = f_boot.render("Finishing The TQP", True, white)
                    self.game_canvas.blit(loading_render, (140, 610))
                    rect_width += 1
            else:
                if play_sfx == 1:
                    play_sfx = 2  # Avoids loop
                boot_sound.stop()  # Stops previous sound effect
                if play_sfx != 3:  # Plays the sound effect once
                    pg.mixer.Channel(0).play(boot_finished)
                    play_sfx = 3  # Avoids loop
                loading_render = f_boot.render("LOADING COMPLETE", True, white)
                self.game_canvas.blit(loading_render, (140, 610))
                rect_width = self.width - 300
                self.fade_out = True
                self.next_level = 1
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            pg.display.update()
