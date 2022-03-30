# Daniel Zhuo
# Module - Button

from bin.blit_tools import draw_text
from bin.colours import *
from pygame import gfxdraw


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


# ------------------------------------------------------------------------------------------------------------------
class BackButton(object):
    def __init__(self, canvas, clr_filled, tri_x1=20, tri_y1=50):
        self.canvas = canvas
        self.clr = white
        self.clr_filled = clr_filled
        # Left Point
        self.tri_x1 = tri_x1
        self.tri_y1 = tri_y1
        # Bottom Right
        self.tri_x2 = tri_x1 + 55
        self.tri_y2 = tri_y1 - 35
        # Top Right
        self.tri_x3 = tri_x1 + 55
        self.tri_y3 = tri_y1 + 35

    def run(self, mx, my, clr, click):
        """Function to run Credits menu
        Args:
            mx:int:
                x position of mouse
            my:int:
                y position of mouse
        """
        # Draw Triangle
        button = pg.draw.polygon(self.canvas, self.clr, [[self.tri_x1, self.tri_y1], [self.tri_x2, self.tri_y2], [self.tri_x3, self.tri_y3]])
        # # Draw Anti-Aliased Triangle
        gfxdraw.aatrigon(self.canvas, self.tri_x1, self.tri_y1, self.tri_x2, self.tri_y2, self.tri_x3, self.tri_y3, self.clr)  # Antialiasing

        # Check for mouse hover
        if button.collidepoint((mx, my)):
            self.clr = self.clr_filled
            if click:
                return True
        else:
            self.clr = clr
