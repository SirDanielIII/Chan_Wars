import os
import random
import sys
import time

from pygame import gfxdraw

from bin.blit_tools import draw_text_left
from bin.classes.level import Level
from bin.classes.stopwatch import Timer
from bin.colours import *


class Boot(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.config = config
        self.next_level = None
        self.task_timer = None
        self.task_timer_delay = None
        self.half_update = None
        self.rect_width_add = None
        self.bar_end = None
        self.rect_width = None
        self.task_num = None
        self.task_text = None
        self.messages = None
        self.msg = None

    def reload(self):
        self.next_level = 1
        self.task_timer = Timer()
        self.task_timer_delay = 0.2
        self.half_update = True
        self.rect_width_add = 2
        self.bar_end = self.width - 300
        self.rect_width = 0
        self.task_num = 1
        self.task_text = "Launching Game"
        self.messages = [
            "\"Many Daniels were hurt in\n  the making of this game.\"",
            "\"Wait where did the first game go?\"",
            "\"Where is the promised sequel?\"",
            "\"For some reason our \n teachers consented to this.\"",
            "\"I apologize for de-facing Stan Lee.\"",
            "\"Don't show this game to your children.\"",
            "\"The game only looks good \n because it's composed of images.\"",
            "\"OMG a loading screen so kool (UwU)\"",
            "\"The end is never the end is never the end.\"",
            "\"There are no regrets in making this.\"",
            "\"You like math.\"",
            "\"This game actually utilized functions.\"",
            "\"This loading screen is \n actually doing something\"",
            "\"A quadrilateral is given in space, such that \n its edges are tangent to a sphere. Prove that \n all the points of tangency lie in one plane.\""
        ]
        self.msg = self.messages[random.randint(0, len(self.messages) - 1)]
        self.alpha_game = 255

    def run(self):
        # ----------------------------------------------------------------------------------------------------------------------
        boot_finished = pg.mixer.Sound(os.getcwd() + "/resources/boot_sfx/boot_confirm.mp3")
        boot_finished.set_volume(0.4)
        finished = False
        # ----------------------------------------------------------------------------------------------------------------------
        game_logo = pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/logo_chan_wars_2.png"), (812, 243)).convert_alpha()
        dev_logo = pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/logo_daniel^2.png"), (600, 600)).convert_alpha()
        # ----------------------------------------------------------------------------------------------------------------------
        f_boot = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 75)
        f_message = pg.font.Font(os.getcwd() + "/resources/Herculanum_LT_Pro_Roman.TTF", 35)
        # ----------------------------------------------------------------------------------------------------------------------
        start_ticks = pg.time.get_ticks()
        milliseconds = pg.USEREVENT
        pg.time.set_timer(milliseconds, 10)
        # ----------------------------------------------------------------------------------------------------------------------
        self.reload()
        # ----------------------------------------------------------------------------------------------------------------------
        while True:
            # Framerate Independence
            dt = time.time() - self.last_time
            dt *= 60  # Delta time - 60fps physics
            self.last_time = time.time()
            # ----------------------------------------------------------------------------------------------------------
            task_delay = (pg.time.get_ticks() - start_ticks) / 1000  # Timer
            # ----------------------------------------------------------------------------------------------------------
            for event in pg.event.get():
                pressed = pg.key.get_pressed()  # Gathers the state of all keys pressed
                if event.type == pg.QUIT or pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == milliseconds:  # Timers
                    self.task_timer.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens(pg.Color("#171717"))
            # ------------------------------------------------------------------------------------------------------------------
            self.draw_message(self.msg, f_message, white, 140, self.game_canvas)
            self.game_canvas.blit(game_logo, (140, 115))
            # ------------------------------------------------------------------------------------------------------------------
            if task_delay > 0.5:
                self.task_timer.time_start()
                if self.rect_width >= self.bar_end:
                    self.rect_width_add = 0
                    self.rect_width = self.bar_end
                else:
                    self.rect_width_add = 13 / self.task_num
                # ------------------------------------------------------------------------------------------------------------------
                match self.task_num:
                    case 1:
                        self.task_text = "Loading Global Config File"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_global_conf()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 2:
                        self.task_text = "Loading Level Configs"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_level_confs()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 3:
                        self.task_text = "Loading Boss Configs"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_boss_confs()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 4:
                        self.task_text = "Importing Menu Images"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_menus()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 5:
                        self.task_text = "Hiring the Bosses"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_boss_select()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 6:
                        self.task_text = "Gathering the Chans"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_chan_cards()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 7:
                        self.task_text = "Hanging Up Paintings"
                        self.rect_width += self.rect_width_add
                        if self.half_update:
                            self.msg = self.messages[random.randint(0, len(self.messages) - 1)]
                            self.half_update = False
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_backgrounds()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 8:
                        self.task_text = "Loading Boss Images"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_bosses()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 9:
                        self.task_text = "Facing the Monster"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_enemies()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 10:
                        self.task_text = "Determining the Endgame"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_end_screens()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 11:
                        self.task_text = "Loading Fonts"
                        self.rect_width += self.rect_width_add
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_fonts()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 12:
                        self.task_text = "Loading Complete"
                        self.rect_width = self.bar_end
                        if not finished:
                            pg.mixer.Channel(1).play(boot_finished)
                            finished = True
                        if self.task_timer.seconds > self.task_timer_delay + 0.5:
                            self.fade_out = True
            # ------------------------------------------------------------------------------------------------------------------
            # Draw Loading Bar
            draw_text_left(self.task_text, white, f_boot, self.game_canvas, 140, 610)
            pg.draw.rect(self.game_canvas, white, (150, self.height - 200, self.rect_width, 50))
            gfxdraw.rectangle(self.game_canvas, (140, self.height - 210, self.width - 280, 70), white)
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            pg.display.update()

    # ----------------------------------------------------------------------------------------------------------------------
    def draw_message(self, message, font, colour, x, screen):
        lines = ["", "", ""]
        for idx, i in enumerate(message.splitlines()):
            lines[idx] = i
        draw_text_left(lines[0], colour, font, screen, x, self.height - 490)
        draw_text_left(lines[1], colour, font, screen, x, self.height - 450)
        draw_text_left(lines[2], colour, font, screen, x, self.height - 410)
