# Daniel Zhuo
# Module - Button

from pygame import gfxdraw

from bin.blit_tools import draw_text_center, draw_text_left
from bin.colours import *


class ButtonRect(object):
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
        self.selected = False
        self.hovered = False

    def check_hover(self):
        """This method is built to only fire once when the mouse hovers on top of the button"""
        if self.selected and not self.hovered:
            self.hovered = True
            return True
        return False

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
            self.selected = True
        else:
            self.selected = False
            self.hovered = False
        # Draw
        self.canvas.blit(self.overlay, (self.x, self.y))
        draw_text_center(self.text, self.text_clr, self.text_font, self.canvas, self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2 - 2)


class OptionsButton(object):
    def __init__(self, canvas, x, y, w, h, stroke_size, clr_outer_default, clr_outer_highlight, clr_inner_off, clr_inner_on, text, text_font, text_clr):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.inner_rect = pg.Rect(x + stroke_size / 2, y + stroke_size / 2, w - stroke_size, h - stroke_size)
        self.outer_rect = pg.Rect(x, y, w, h)
        self.clr_outer_default = clr_outer_default
        self.clr_outer_highlight = clr_outer_highlight
        self.clr_inner_off = clr_inner_off
        self.clr_inner_on = clr_inner_on
        self.text = text
        self.text_font = text_font
        self.text_clr = text_clr
        self.clicked = False
        self.clr_outer = clr_outer_default
        self.locked = False
        self.selected = False
        self.hovered = False

    def check_hover(self):
        """This method is built to only fire once when the mouse hovers on top of the button"""
        if self.selected and not self.hovered:
            self.hovered = True
            return True
        return False

    def check_click(self, mx, my, click, lock=False):
        """
        Args:
            mx:int:
                x position of mouse
            my:int:
                y position of mouse
            click::boolean:
                Button press boolean from event loop
            lock::boolean:
                Whether to lock the button or not
        Returns:
            True/False to indicate if the button was pressed or not
        Notes:
            Call this method before draw_button()
        """
        if self.outer_rect.collidepoint(mx, my):
            self.selected = True
            if click and not self.locked:
                if not lock:
                    self.clicked = not self.clicked
                    return True
                self.clicked = True
                self.locked = True
                return True
        elif not self.outer_rect.collidepoint((mx, my)):
            self.selected = False
            self.hovered = False
        return False

    def turn_off_button(self):
        self.clicked = False
        self.locked = False

    def draw_button(self, mx, my, force_highlight=False):
        if self.outer_rect.collidepoint((mx, my)):  # Draw Highlights
            if self.clicked and not force_highlight:
                self.clr_outer = self.clr_outer_default
            else:
                self.clr_outer = self.clr_outer_highlight
        else:  # Don't draw highlights
            self.clr_outer = self.clr_outer_default

        pg.draw.rect(self.canvas, self.clr_outer, self.outer_rect)
        pg.draw.rect(self.canvas, self.clr_inner_off if not self.clicked else self.clr_inner_on, self.inner_rect)
        draw_text_left(self.text, self.text_clr, self.text_font, self.canvas, self.outer_rect.x + self.outer_rect.w * 2, self.outer_rect.y + (self.outer_rect.height - 40) / 2)


class SliderButton(object):
    def __init__(self, canvas, max_pos, min_pos, button_y, button_w, button_h, stroke_size, clr_outer_default, clr_outer_highlight, clr_inner_off, clr_inner_on,
                 slider_size, slider_clr):
        self.canvas = canvas
        self.max_pos = max_pos
        self.min_pos = min_pos
        self.button_w = button_w
        self.stroke_size = stroke_size
        self.clr_outer_default = clr_outer_default
        self.clr_outer_highlight = clr_outer_highlight
        self.clr_inner_off = clr_inner_off
        self.clr_inner_on = clr_inner_on
        self.clr_outer = clr_outer_default
        self.slider_size = slider_size
        self.clr_slider = slider_clr
        self.locked = False
        self.selected = False
        self.hovered = False
        self.activated = True
        self.current_pos = max_pos - self.button_w / 2
        self.inner_rect = pg.Rect(self.current_pos, button_y + self.stroke_size / 2, button_w - self.stroke_size, button_h - self.stroke_size)
        self.outer_rect = pg.Rect(max_pos, button_y, button_w, button_h)
        self.slider_rect = pg.Rect(min_pos, button_y + ((button_h - self.slider_size) / 2), max_pos - min_pos, self.slider_size)

    def check_hover(self):
        """This method is built to only fire once when the mouse hovers on top of the button"""
        if self.selected and not self.hovered:
            self.hovered = True
            return True
        return False

    def lock_slider(self):
        self.locked = True

    def unlock_slider(self):
        self.locked = False

    def check_click(self, mx, my, click):
        if self.outer_rect.collidepoint(mx, my) and not self.locked:
            return True if click else False

    def move_buttons(self, mx, my):
        if self.activated:
            if self.min_pos <= mx <= self.max_pos:
                self.current_pos = mx - self.button_w / 2
            elif mx < self.min_pos:
                self.current_pos = self.min_pos - self.button_w / 2
            elif mx > self.max_pos - self.button_w / 2:
                self.current_pos = self.max_pos - self.button_w / 2

    def draw_slider(self, mx, my, hold):
        if self.outer_rect.collidepoint(mx, my) and not self.locked:  # Draw Highlights
            self.activated = True
            self.selected = True
            self.clr_outer = self.clr_outer_highlight
        else:  # Don't draw highlights
            self.clr_outer = self.clr_outer_default
            self.selected = False
            self.hovered = False
        if not hold:
            self.activated = False
        self.move_buttons(mx, my)
        # Adjust button x-values
        self.outer_rect.x = self.current_pos
        self.inner_rect.x = self.current_pos + self.stroke_size / 2
        # Slider Line
        pg.draw.rect(self.canvas, self.clr_slider, self.slider_rect)
        # Button
        pg.draw.rect(self.canvas, self.clr_outer, self.outer_rect)
        pg.draw.rect(self.canvas, self.clr_inner_off if not self.locked else self.clr_inner_on, self.inner_rect)


# ------------------------------------------------------------------------------------------------------------------
class ButtonTriangle(object):
    def __init__(self, canvas, clr_filled, tri_x1=20, tri_y1=50, pointing="left"):
        self.canvas = canvas
        self.clr = white
        self.clr_filled = clr_filled
        # Pointy Part
        self.tri_x1 = tri_x1
        self.tri_y1 = tri_y1
        if pointing == "left":
            # Bottom Right
            self.tri_x2 = tri_x1 + 55
            self.tri_y2 = tri_y1 - 35
            # Top Right
            self.tri_x3 = tri_x1 + 55
            self.tri_y3 = tri_y1 + 35
        elif pointing == "right":
            # Bottom Left
            self.tri_x2 = tri_x1 - 55
            self.tri_y2 = tri_y1 + 35
            # Top Left
            self.tri_x3 = tri_x1 - 55
            self.tri_y3 = tri_y1 - 35
        self.selected = False
        self.hovered = False

    def check_hover(self):
        """This method is built to only fire once when the mouse hovers on top of the button"""
        if self.selected and not self.hovered:
            self.hovered = True
            return True
        return False

    def run(self, mx, my, clr, click):
        """Function to run Credits menu
        Args:
            mx:int:
                x position of mouse
            my:int:
                y position of mouse
            clr:tuple:
                Colour
            click:bool:
                Detect mouse click
        """
        # Draw Triangle
        button = pg.draw.polygon(self.canvas, self.clr, [[self.tri_x1, self.tri_y1], [self.tri_x2, self.tri_y2], [self.tri_x3, self.tri_y3]])
        # # Draw Anti-Aliased Triangle
        gfxdraw.aatrigon(self.canvas, self.tri_x1, self.tri_y1, self.tri_x2, self.tri_y2, self.tri_x3, self.tri_y3, self.clr)  # Antialiasing

        # Check for mouse hover
        if button.collidepoint((mx, my)):
            self.clr = self.clr_filled
            self.selected = True
            if click:
                return True
        else:
            self.clr = clr
            self.selected = False
            self.hovered = False
