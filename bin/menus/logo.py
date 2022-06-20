import os
import time

from bin.blit_tools import center_blit_image
from bin.classes.level import Level
from bin.colours import *


class Logo(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
        self.config = config
        self.audio = audio
        self.transition_speed = 3
        self.play = None

    def reload(self):
        self.play = True
        self.next_level = 2

    def run(self):
        dev_logo = pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/logo_daniel^2.png"), (600, 600)).convert_alpha()
        logo_music = pg.mixer.Sound(os.getcwd() + "/resources/audio/boot/boot_logo.mp3")
        logo_music.set_volume(0.6)
        finished = False
        # ----------------------------------------------------------------------------------------------------------------------
        start_ticks = pg.time.get_ticks()
        # ----------------------------------------------------------------------------------------------------------------------
        self.reload()
        # ----------------------------------------------------------------------------------------------------------------------
        while 1:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            # ----------------------------------------------------------------------------------------------------------
            task_delay = (pg.time.get_ticks() - start_ticks) / 1000  # Timer
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    self.config.shutdown(None)
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens(pg.Color("#171717"))
            center_blit_image(self.game_canvas, dev_logo, self.width / 2, self.height / 2)
            # ------------------------------------------------------------------------------------------------------------------
            if task_delay > 0.1 and self.play:
                self.audio.dj(None, None, [None, None], 100, False, 0, logo_music)
                self.play = False
            # ------------------------------------------------------------------------------------------------------------------
            if task_delay > 4.1:
                self.fade_out = True
                self.transition_speed = 4
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.config.FPS)
            pg.display.update()
