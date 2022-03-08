# Daniel Zhuo
# Module - Button

import pygame as pg

from ..tools.blit_tools import draw_text


class Button(object):
    def __init__(self, canvas, rect, clr, text_font, text_clr, stroke1=0, stroke2=0):
        self.canvas = canvas
        self.rect = rect
        self.rect_clr = clr
        self.text_font = text_font
        self.text_clr = text_clr
        self.rect_stroke = stroke1
        self.text_stroke = stroke2

    def check_click(self, mx, my, click):
        """
        Args:
            mx:int:
                x position of mouse
            my:int:
                y position of mouse
            click::boolean:
                Button press from event loop
        Returns:
            True/False to indicate if the button was pressed or not
        Notes:
            Call this method before draw_button()
        """
        if self.rect.collidepoint((mx, my)):
            pg.draw.rect(self.canvas, (255, 255, 255, 50), self.rect)
            if click:
                return True
            return False

    def draw_button(self, text):
        """
        Args:
            text::string:
                Text to display
        """
        pg.draw.rect(self.canvas, self.rect_clr, self.rect)
        draw_text(text, self.text_clr, self.text_font, self.canvas, self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2 - 2)
