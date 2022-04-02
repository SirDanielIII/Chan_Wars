import pygame as pg

from bin.blit_tools import draw_rect_outline


class HealthBarLeft(object):
    def __init__(self, screen, dimensions, max_hp, config, clr_main, clr_stroke, stroke_size=3,
                 back_rect=False, clr_back_rect=(255, 0, 0),
                 highlight=False, clr_highlight=pg.Color("#FFFF55")):
        self.screen = screen
        self.x = dimensions.x
        self.y = dimensions.y
        self.w = dimensions.w
        self.h = dimensions.h
        self.max_hp = self.hp = self.hp_last = max_hp
        self.config = config
        self.clr_main = clr_main
        self.clr_stroke = clr_stroke
        self.stroke_size = stroke_size
        self.back_rect = back_rect
        self.clr_back_rect = clr_back_rect
        self.highlight = highlight
        self.clr_highlight = clr_highlight

    def render_back(self):
        if self.back_rect:
            pg.draw.rect(self.screen, self.clr_back_rect, pg.Rect(self.x, self.y, self.w, self.h))

    def render_highlight(self, speed, dt):
        if self.highlight:
            if self.hp_last > self.hp:
                self.hp_last -= speed * dt
            elif self.hp_last < self.hp:
                self.hp_last = self.hp
            pg.draw.rect(self.screen, self.clr_highlight, pg.Rect((self.x, self.y, self.w * (self.hp_last / self.max_hp), self.h)))

    def width_proportional(self):
        # The width of the bar is tied to the percentage loss of the current value compared to the max value
        return self.w * (self.hp / self.max_hp)

    def render(self, speed, dt):
        self.render_back()
        self.render_highlight(speed, dt)
        pg.draw.rect(self.screen, self.clr_main, pg.Rect(self.x, self.y, self.width_proportional(), self.h))
        draw_rect_outline(self.screen, self.clr_stroke, pg.Rect(self.x - self.stroke_size, self.y - self.stroke_size, self.w + self.stroke_size * 2, self.h + self.stroke_size * 2))
