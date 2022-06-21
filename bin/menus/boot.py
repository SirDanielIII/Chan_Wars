import os
import random
import time

from pygame import gfxdraw

from bin.blit_tools import draw_text_left
from bin.classes.level import Level
from bin.classes.stopwatch import Timer
from bin.colours import *


class Boot(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
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
        self.transition_speed = 5

    def run(self):
        # ----------------------------------------------------------------------------------------------------------------------
        boot_finished = pg.mixer.Sound(os.getcwd() + "/resources/audio/boot/boot_confirm.mp3")
        boot_finished.set_volume(0.4)
        boot_hdd = pg.mixer.Sound(os.getcwd() + "/resources/audio/boot/emily_is_away_hdd_bootup.wav")
        finished = False
        # ----------------------------------------------------------------------------------------------------------------------
        game_logo = pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/logo_chan_wars_2.png"), (812, 243)).convert_alpha()
        chan_logo = pg.transform.smoothscale(pg.image.load(os.getcwd() + "/resources/icon.png"), (421, 419)).convert_alpha()
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
        self.audio.dj(None, None, ["", 0], 100, False, 0, boot_hdd)
        while 1:
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
                    self.config.shutdown(None)
                if event.type == milliseconds:  # Timers
                    self.task_timer.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens(pg.Color("#171717"))
            # ------------------------------------------------------------------------------------------------------------------
            self.draw_message(self.msg, f_message, white, 140, self.game_canvas)
            self.game_canvas.blit(game_logo, (140, 115))
            self.game_canvas.blit(chan_logo, (1018, 115))
            # ------------------------------------------------------------------------------------------------------------------
            if task_delay > 0.5:
                self.task_timer.time_start()
                if self.rect_width >= self.bar_end:
                    self.rect_width_add = 0
                    self.rect_width = self.bar_end
                else:
                    self.rect_width_add = 14 / self.task_num
                # ------------------------------------------------------------------------------------------------------------------
                match self.task_num:
                    case 1:
                        self.task_text = "Loading Global Config File"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_global_conf()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 2:
                        self.task_text = "Applying Global Changes"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            if self.config.fullscreen:
                                self.surface = pg.display.set_mode((self.width, self.height), flags=pg.HWSURFACE and pg.DOUBLEBUF and pg.SRCALPHA and pg.FULLSCREEN)
                            if self.config.skip_intro:
                                self.next_level = 2
                            if self.config.fast_boot:
                                self.task_timer_delay = 0.02
                            self.audio.enable_music = self.config.global_conf["settings"]["audio"]["enable_music"]
                            self.audio.enable_sfx = self.config.global_conf["settings"]["audio"]["enable_sfx"]
                            self.audio.music_vol = self.config.global_conf["settings"]["audio"]["music_vol"]
                            self.audio.sfx_vol = self.config.global_conf["settings"]["audio"]["sfx_vol"]
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 3:
                        self.task_text = "Loading Level Configs"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_level_confs()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 4:
                        self.task_text = "Loading Boss Configs"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_boss_confs()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 5:
                        self.task_text = "Importing Menu Images"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_menus()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 6:
                        self.task_text = "Hiring the Bosses"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_boss_select()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 7:
                        self.task_text = "Gathering the Chans"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_chan_cards()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 8:
                        self.task_text = "Hanging Up Paintings"
                        self.rect_width += self.rect_width_add * dt
                        if self.half_update:
                            self.msg = self.messages[random.randint(0, len(self.messages) - 1)]
                            self.half_update = False
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_backgrounds()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 9:
                        self.task_text = "Loading Boss Images"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_bosses()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 10:
                        self.task_text = "Facing the Monster"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_enemies()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 11:
                        self.task_text = "Determining the Endgame"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_end_screens()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 12:
                        self.task_text = "Copy Pasting Images"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_img_ui()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 13:
                        self.task_text = "Loading Fonts"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_fonts()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 14:
                        self.task_text = "Loading Menu Soundtrack"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_menu()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 15:
                        self.task_text = "Loading Bipolar Noises"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_completion()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 16:
                        self.task_text = "Loading Game SFX"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_game()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 17:
                        self.task_text = "Loading Button Noises"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_interact()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 18:
                        self.task_text = "Devil Chan Misses Angel Chan"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_lvl_1()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 19:
                        self.task_text = "Singing Russian Music"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_lvl_2()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 20:
                        self.task_text = "Running Away From Mr. Phone"
                        self.rect_width += self.rect_width_add * dt
                        if self.task_timer.seconds > self.task_timer_delay:
                            self.config.load_audio_lvl_3()
                            self.task_timer.time_reset()
                            self.task_num += 1
                    case 21:
                        self.task_text = "Loading Complete"
                        self.rect_width = self.bar_end
                        if not finished:
                            self.audio.dj(None, None, ["sfx", 0], 800, False, 1, boot_finished)
                            finished = True
                        if self.task_timer.seconds > self.task_timer_delay + 0.5:
                            self.fade_out = True
            # ------------------------------------------------------------------------------------------------------------------
            # Draw Loading Bar
            draw_text_left(self.task_text, white, f_boot, self.game_canvas, 140, 610)
            pg.draw.rect(self.game_canvas, white, (150, self.height - 200, self.rect_width, 50))
            gfxdraw.rectangle(self.game_canvas, (140, self.height - 210, self.width - 280, 70), white)
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # --------------------------------------------------------------------------------------------------------------
            if self.transition_out("game", self.game_canvas, dt):
                self.restore()
                self.transition_speed = 3
                self.next_level = 4
                return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.config.FPS)
            pg.display.update()

    # ----------------------------------------------------------------------------------------------------------------------
    def draw_message(self, message, font, colour, x, screen):
        lines = ["", "", ""]
        for idx, i in enumerate(message.splitlines()):
            lines[idx] = i
        draw_text_left(lines[0], colour, font, screen, x, self.height - 490)
        draw_text_left(lines[1], colour, font, screen, x, self.height - 450)
        draw_text_left(lines[2], colour, font, screen, x, self.height - 410)
