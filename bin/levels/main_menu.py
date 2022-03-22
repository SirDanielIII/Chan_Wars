import pygame as pg
import os
import sys
import time

from ..classes.level import Level
from ..tools.colours import *
from ..classes.button import Button
#test

gameOn = False


class MainMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time)
        # Fonts
        self.f_regular_small = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 40)
        self.f_regular = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 50)
        self.f_regular_big = pg.font.Font(os.getcwd() + "/resources/Herculanum-Regular.ttf", 100)
        # Create Button Class
        self.b_play_game = Button(self.text_canvas, 100, 400, 650, 150, blue, "Play Game", self.f_regular_big, white)
        self.b_options = Button(self.text_canvas, 100, 600, 300, 100, blue, "Options", self.f_regular, white)
        self.b_help = Button(self.text_canvas, 450, 600, 300, 100, blue, "How to Play", self.f_regular_small, white)
        self.b_credits = Button(self.text_canvas, 100, 750, 300, 100, blue, "Credits", self.f_regular, white)
        self.b_quit = Button(self.text_canvas, 450, 750, 300, 100, blue, "Quit", self.f_regular, white)
        self.buttons = [self.b_play_game, self.b_options, self.b_help, self.b_credits, self.b_quit]
        self.test = pg.Surface((1280, 720), flags=pg.HWACCEL and pg.DOUBLEBUF)


    def run(self):
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            self.click = False
            mx, my = pg.mouse.get_pos()  # Get mouse position
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
                    if event.button == 1:  # Left Mouse Button
                        self.click = True

            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            self.test.fill((0, 255, 255))
            self.surface.blit(self.test, ((self.width - self.test.get_width()) / 2, (self.height - self.test.get_height()) / 2))
            # ------------------------------------------------------------------------------------------------------------------
            for i in self.buttons:
                i.draw_button(mx, my)
                if i.check_click(mx, my, self.click):
                    print("done")
            if self.b_play_game.check_click(mx, my, self.click):
                return 2
            if self.b_quit.check_click(mx, my, self.click):
                return 6
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
