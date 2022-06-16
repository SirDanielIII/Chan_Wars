import sys
import time

from bin.classes.stopwatch import Timer
from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *


class Death(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.background = None
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        self.death_stopwatch = Timer()

    def set_background(self, winning_state):
        self.death_stopwatch.time_reset()
        self.background = self.config.img_end_screens[winning_state]

    def reload(self):
        self.alpha_game = 255

    def run(self):
        self.reload()
        milliseconds = pg.USEREVENT
        pg.time.set_timer(milliseconds, 10)
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
                if event.type == milliseconds:
                    self.death_stopwatch.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            if not self.death_stopwatch.started_timer:
                self.death_stopwatch.time_start()
            if self.death_stopwatch.seconds > 1:
                self.background.set_alpha((self.death_stopwatch.seconds - 1) * 250)
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
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
