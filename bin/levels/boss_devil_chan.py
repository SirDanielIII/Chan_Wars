import sys
import time
import os

from bin.classes.buttons import ButtonTriangle
from bin.classes.level import Level
from bin.colours import *
from bin.classes.bosses import DevilChan as dchan


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)

    def run(self):
        configuration = self.config.get_config()["bosses"]["DevilChan"]
        devil_chan_boss = dchan(self.surface, configuration)
        while True:
            damage_taken = 0
            boss_turn = True
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ------------------------------------------------------------------------------------------------------------------
            boss_state = devil_chan_boss.update(damage_taken, pg.time.get_ticks(), boss_turn)
            devil_chan_boss.trigger()
            action = devil_chan_boss.act()
            action_type = action[0]
            action_quote = action[1][1]
            attack_damage = action[1][0]
            print(boss_state, action, action_type, action_quote, attack_damage)
            # ------------------------------------------------------------------------------------------------------------------
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
            self.game_canvas.fill((255, 0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if self.back_button.run(mx, my, cw_light_blue, self.click):
                self.fade_out = True
                self.next_level = 1
            # ------------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
