from abc import ABC, abstractmethod

import pygame as pg

from ..tools.colours import *


class Level(ABC):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        self.width = width
        self.height = height
        self.surface = surface
        self.game_canvas = game_canvas
        self.clock = clock
        self.FPS = fps
        self.last_time = last_time
        self.config = config
        self.text_canvas = pg.Surface((width, height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.alpha_game = 0
        self.alpha_text = 255
        self.transition = 1  # 0 -> Nothing | 1 -> Fade In | 2 -> Fade Out
        self.transition_speed = 3  # 0 -> Nothing | 1 -> Fade In | 2 -> Fade Out
        self.next_level = None
        self.click = False
        self.screen_offset = [0, 0]

    def fill_screens(self):
        """Fill the surfaces to avoid smudging"""
        self.surface.fill(black)
        # Fill with transparent colour for Alpha
        self.game_canvas.fill((0, 0, 0, 0))
        if self.alpha_text != 0:
            self.text_canvas.fill((0, 0, 0, 0))

    def blit_screens(self):
        """Blit the surfaces; don't blit text_canvas if it's not visible"""
        if self.alpha_text != 0:
            self.game_canvas.blit(self.text_canvas, (0, 0))
        self.surface.blit(self.game_canvas, (0 + self.screen_offset[0], 0 + self.screen_offset[1]))

    # ------------------------------------------------------------------------------------------------------------------
    def fade_screen_in(self, screen_type, screen, speed, dt):
        """Screen fade manager - in
        Args:
            screen_type:string:
                Used to determine which surface to fade in
            screen:surface:
                Specify the screen to be faded in
            speed:float:
                Speed at which the fade is executed
            dt:float:
                Value calculated from last_time for Framerate Independence
        """
        match screen_type:
            case "game":
                screen.set_alpha(self.alpha_game)
                if self.alpha_game < 255:
                    self.alpha_game += speed * dt
                    return False
                else:
                    self.alpha_game = 255
                    return True
            case "text":
                screen.set_alpha(self.alpha_text)
                if self.alpha_text < 255:
                    self.alpha_text += speed * dt
                    return False
                else:
                    self.alpha_text = 255
                    return True

    def fade_screen_out(self, screen_type, screen, speed, dt):
        """Screen fade manager - out
        Args:
            screen_type:string:
                Used to determine which surface to fade out
            screen:surface:
                Specify the screen to be faded out
            speed:float:
                Speed at which the fade is executed
            dt:float:
                Value calculated from last_time for Framerate Independence
        """
        match screen_type:
            case "game":
                screen.set_alpha(self.alpha_game)
                if self.alpha_game > 0:
                    self.alpha_game -= speed * dt
                    return False
                else:
                    self.alpha_game = 0
                    return True
            case "text":
                screen.set_alpha(self.alpha_text)
                if self.alpha_text > 0:
                    self.alpha_text -= speed * dt
                    return False
                else:
                    self.alpha_text = 0
                    return True

    def transition_lvl(self, screen_type, screen, dt):
        if self.transition == 1:
            if self.fade_screen_in(screen_type, screen, self.transition_speed, dt):
                self.transition = 0
        elif self.transition == 2:
            if self.fade_screen_out(screen_type, screen, self.transition_speed, dt):
                self.transition = 0
                return self.next_level

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def run(self):
        pass
