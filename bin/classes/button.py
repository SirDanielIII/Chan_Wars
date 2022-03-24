# Daniel Zhuo
# Module - Button

import pygame as pg

from ..tools.blit_tools import draw_text


class Button(object):
    def __init__(self, canvas, x, y, w, h, clr, text, text_font, text_clr, stroke1=0, stroke2=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        self.rect_clr = clr
        self.text = text
        self.text_font = text_font
        self.text_clr = text_clr
        self.rect_stroke = stroke1
        self.text_stroke = stroke2
        self.overlay = pg.Surface((w, h), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()

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
        if self.rect.collidepoint((mx, my)) and click:
            return True
        return False

    def draw_button(self, mx, my):
        self.overlay.fill((0, 0, 0, 0))
        pg.draw.rect(self.canvas, self.rect_clr, self.rect)
        # Check for mouse hover
        if self.rect.collidepoint((mx, my)):
            self.overlay.fill((255, 255, 255, 50))
        # Draw
        self.canvas.blit(self.overlay, (self.x, self.y))
        draw_text(self.text, self.text_clr, self.text_font, self.canvas, self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2 - 2)
