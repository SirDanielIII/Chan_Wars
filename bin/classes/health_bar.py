import pygame as pg


class HealthBar(object):
    def __init__(self, dimensions, max_hp, config, clr_main, clr_stroke, stroke_size=3,
                 back_rect=False, clr_back_rect=(255, 0, 0),
                 highlight=False, clr_highlight=pg.Color("#FFFF55")):
        self.x = dimensions.x
        self.y = dimensions.y
        self.w = dimensions.w
        self.h = dimensions.h
        self.max_hp = self.hp = self.hp_last = max_hp
        self.config = config

    def render(self):
        pass

    # def draw_bar_value_left(screen, max_current, current, rectangle, clr_main, clr_stroke, stroke_size=3,
    #                         back=False, clr_back=(255, 0, 0),
    #                         highlight=False, last_current=0, clr_highlight=pg.Color("#FFFF55")):
    #     if back:
    #         pg.draw.rect(screen, clr_back, pg.Rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3]))
    #     if highlight:
    #         bar_highlight = pg.Rect(rectangle[0], rectangle[1], rectangle[2] * (last_current / max_current), rectangle[3])
    #         pg.draw.rect(screen, clr_highlight, bar_highlight)
    #     new_w = rectangle[2] * (current / max_current)  # The width of the bar is tied to the percentage loss of the current value compared to the max value
    #     pg.draw.rect(screen, clr_main, pg.Rect(rectangle[0], rectangle[1], new_w, rectangle[3]))
    #     draw_rect_outline(screen, clr_stroke, pg.Rect(rectangle[0] - stroke_size, rectangle[1] - stroke_size, rectangle[2] + stroke_size * 2, rectangle[3] + stroke_size * 2))
