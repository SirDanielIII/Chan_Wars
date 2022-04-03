import pygame as pg

from bin.blit_tools import draw_rect_outline


class HealthBar(object):
    def __init__(self, screen, dimensions, max_hp, clr_main, clr_stroke, stroke_size=3,
                 back_rect=False, clr_back_rect=pg.Color("#FF5555"),
                 highlight=False, clr_highlight=pg.Color("#FFFF55")):
        self.screen = screen
        self.x = dimensions.x
        self.y = dimensions.y
        self.w = dimensions.w
        self.h = dimensions.h
        self.max_hp = self.hp = self.hp_last = max_hp  # Set initial HP values
        self.clr_main = clr_main
        self.clr_stroke = clr_stroke
        self.stroke_size = stroke_size
        self.back_rect = back_rect
        self.clr_back_rect = clr_back_rect
        self.highlight = highlight
        self.clr_highlight = clr_highlight

    # ------------------------------------------------------------------------------------------------------------------
    def render_back(self):
        if self.back_rect:
            pg.draw.rect(self.screen, self.clr_back_rect, pg.Rect(self.x, self.y, self.w, self.h))

    # ------------------------------------------------------------------------------------------------------------------
    def render_highlight(self, speed, dt, right):
        if self.highlight:
            if self.hp_last > self.hp:
                self.hp_last -= speed * dt
            elif self.hp_last < self.hp:
                self.hp_last = self.hp
        # ------------------------------------------------------------------------------------------------------------------
            if not right:
                pg.draw.rect(self.screen, self.clr_highlight,
                             pg.Rect((self.x,
                                      self.y,
                                      self.w * (self.hp_last / self.max_hp),
                                      self.h)))
        # ------------------------------------------------------------------------------------------------------------------
            else:
                pg.draw.rect(self.screen, self.clr_highlight,
                             pg.Rect((self.x + (self.w - self.width_proportional(self.hp_last, self.max_hp)),
                                      self.y,
                                      self.width_proportional(self.hp_last, self.max_hp),
                                      self.h)))

    # ------------------------------------------------------------------------------------------------------------------
    def width_proportional(self, var, var_max):
        # The width of the bar is tied to how much the value fits in a range, returned in a percentage (E.G. 0.4)
        return self.w * (var / var_max)

    # ------------------------------------------------------------------------------------------------------------------
    def render(self, hp, speed, dt, right=False):
        self.hp = hp  # Get updated HP
        self.render_back()
        self.render_highlight(speed, dt, right)
        # ------------------------------------------------------------------------------------------------------------------
        draw_rect_outline(self.screen, self.clr_stroke,
                          pg.Rect(self.x - self.stroke_size,
                                  self.y - self.stroke_size,
                                  self.w + self.stroke_size * 2,
                                  self.h + self.stroke_size * 2))
        # ------------------------------------------------------------------------------------------------------------------
        if not right:
            pg.draw.rect(self.screen, self.clr_main,
                         pg.Rect(self.x,
                                 self.y,
                                 self.width_proportional(self.hp, self.max_hp),  # Get new width based on percentage out of MAX WIDTH
                                 self.h))
        # ------------------------------------------------------------------------------------------------------------------
        else:
            pg.draw.rect(self.screen, self.clr_main,
                         pg.Rect(self.x + (self.w - self.width_proportional(self.hp, self.max_hp)),  # Offset by MAX WIDTH - LOST WIDTH
                                 self.y,
                                 self.width_proportional(self.hp, self.max_hp),  # Get new width based on percentage out of MAX WIDTH
                                 self.h))
