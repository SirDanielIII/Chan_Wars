from abc import ABC, abstractmethod

from bin.blit_tools import draw_rect_outline
from bin.colours import *


class Level(ABC):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__()
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
        self.fade_in = True
        self.fade_out = False
        self.transition_speed = 10  # 0 -> Nothing | 1 -> Fade In | 2 -> Fade Out
        self.next_level = None
        self.click = False
        self.screen_offset = [0, 0]
        self.freeze = True

    def restore(self):
        self.fade_in = True
        self.fade_out = False
        self.alpha_game = 0
        self.alpha_text = 255
        self.freeze = True

    def fill_screens(self):
        """Fill the surfaces to avoid smudging"""
        self.surface.fill(black)
        # Fill with transparent colour for Alpha
        self.game_canvas.fill((0, 0, 0, 0))
        if self.alpha_text != 0:
            self.text_canvas.fill((0, 0, 0, 0))

    def blit_screens(self, card_screen=False, card_canvas=None):
        """Blit the surfaces; don't blit text_canvas if it's not visible"""
        if self.alpha_text != 0:
            self.game_canvas.blit(self.text_canvas, (0, 0))
        if card_screen:
            self.game_canvas.blit(card_canvas, (0, 0))
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

    def transition_in(self, screen_type, screen, dt):
        if self.fade_in:
            if self.fade_screen_in(screen_type, screen, self.transition_speed, dt):
                self.fade_in = False

    def transition_out(self, screen_type, screen, dt):
        if self.fade_out:
            if self.fade_screen_out(screen_type, screen, self.transition_speed, dt):
                return True

    @staticmethod
    def bar_percentage(pos, max_pos, percent=True):
        if percent:
            return (pos / max_pos) * 100
        else:
            return pos / max_pos

    @staticmethod
    def bar_pos(pos, min_pos, max_pos, percent=True):
        if percent:
            return ((pos - min_pos) / 100) * max_pos
        else:
            return (pos - min_pos) * max_pos

    @staticmethod
    def draw_bar(screen, og_rect, length, height, clr_main, clr_stroke, stroke_size=3, highlight=False, clr_highlight=pg.Color("#FFFF55")):
        if highlight:
            bar_highlight = pg.Rect(og_rect[0], og_rect[1], length, height)
            pg.draw.rect(screen, clr_highlight, bar_highlight)
        bar_main = pg.Rect(og_rect[0], og_rect[1], length, height)
        pg.draw.rect(screen, clr_main, bar_main)
        draw_rect_outline(screen, clr_stroke, pg.Rect(og_rect[0] - stroke_size, og_rect[1] - stroke_size, og_rect[2] + stroke_size * 2, og_rect[3] + stroke_size * 2))

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def run(self):
        pass
