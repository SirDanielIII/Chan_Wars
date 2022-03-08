import pygame as pg
import os
import sys
import time

from ..classes.level import Level
from ..tools.colours import *
from ..classes.button import Button


class MainMenu(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time)
        # Fonts
        self.f_regular_small = pg.font.Font(os.getcwd() + "/bin/resources/Herculanum-Regular.ttf", 40)
        self.f_regular = pg.font.Font(os.getcwd() + "/bin/resources/Herculanum-Regular.ttf", 50)
        self.f_regular_big = pg.font.Font(os.getcwd() + "/bin/resources/Herculanum-Regular.ttf", 100)
        # Create Button Class
        self.b_play_game = Button(self.text_canvas, pg.Rect(100, 400, 650, 150), blue, self.f_regular_big, white)
        self.b_options = Button(self.text_canvas, pg.Rect(100, 600, 300, 100), blue, self.f_regular, white)
        self.b_help = Button(self.text_canvas, pg.Rect(450, 600, 300, 100), blue, self.f_regular_small, white)
        self.b_credits = Button(self.text_canvas, pg.Rect(100, 750, 300, 100), blue, self.f_regular, white)
        self.b_quit = Button(self.text_canvas, pg.Rect(450, 750, 300, 100), blue, self.f_regular, white)

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
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            # Play Game
            if self.b_play_game.check_click(mx, my, self.click):
                print("Work")

            self.b_play_game.draw_button("Play Game")
            # ------------------------------------------------------------------------------------------------------------------
            # Options
            if self.b_options.check_click(mx, my, self.click):
                print("Work")
            self.b_options.draw_button("Options")
            # ------------------------------------------------------------------------------------------------------------------
            # How to Play
            if self.b_help.check_click(mx, my, self.click):
                print("Work")
            self.b_help.draw_button("How to Play")
            # ------------------------------------------------------------------------------------------------------------------
            # Credits
            if self.b_credits.check_click(mx, my, self.click):
                print("Work")
            self.b_credits.draw_button("Credits")
            # ------------------------------------------------------------------------------------------------------------------
            # Quit Game
            if self.b_quit.check_click(mx, my, self.click):
                print("Work")
            self.b_quit.draw_button("Quit")
            # ------------------------------------------------------------------------------------------------------------------
            # self.game_canvas.fill((255, 255, 255))
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
