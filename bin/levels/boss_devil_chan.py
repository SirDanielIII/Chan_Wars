import random
import sys
import time
import math

from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.classes.stopwatch import Timer
from bin.classes.typewriter import Typewriter
from bin.colours import *
from bin.classes.card_pair import move_pos
from bin.classes.bosses import DevilChan as DChan
import bin.classes.card_pair as card_pair


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config)
        self.back_button = ButtonTriangle(self.game_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = self.height
        self.card_game = False
        self.game_transition_in = False
        self.game_transition_out = False
        self.energy = None
        self.size = self.config.card_size
        self.margins = (20, 30)
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.hp_player = None
        self.damage = 0
        self.hp_bar_player = None
        self.card_complete = [0]
        self.pairs = None
        self.player = card_pair.MatchingScreen(0, None, self.card_canvas)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.boss = None
        self.boss_data = None
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_boss = None
        self.hp_bar_boss = None
        # ------------------------------------------------------------------------------------------------------------------
        # Text Bar Attributes
        self.text_transition_in = False
        self.text_transition_out = False
        self.typewriter_l1 = Typewriter()
        self.typewriter_l2 = Typewriter()
        self.finished = False
        self.update = True
        self.message = 0
        self.align_x = 130
        self.align_y1 = 670
        self.align_y2 = 730
        # ------------------------------------------------------------------------------------------------------------------
        # Event Handler
        self.event = "cinematic"
        self.cinematic = True
        # ------------------------------------------------------------------------------------------------------------------
        # Timer Attributes
        self.timer_dict = {"action": Timer(), "card": Timer(), "cinematic": Timer(), "transition": Timer(), "death": Timer(),
                           "update_delay": Timer()}

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes Initialization
        self.boss_data = self.config.get_config()["level_1"]
        self.boss = DChan(self.boss_data)
        self.boss.load_boss_info()
        self.hp_boss = self.boss_data["boss"]["hp"]
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.hp_boss, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.boss.metadata = self.boss_data
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes Initialization
        self.hp_player = self.boss_data["player"]["hp"]
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.hp_player, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.player.image_list = self.config.image_list
        self.player.columns = self.boss_data["player"]["columns"]
        self.energy = self.boss_data["player"]["energy"]
        self.card_complete = [0]
        self.pairs = None
        # ------------------------------------------------------------------------------------------------------------------
        # Text Bar Attributes
        self.text_transition_in = False
        self.text_transition_out = False
        self.typewriter_l1 = Typewriter()
        self.typewriter_l2 = Typewriter()
        self.finished = False
        self.update = True
        self.message = 0
        self.align_x = 130
        self.align_y1 = 670
        self.align_y2 = 730
        # ------------------------------------------------------------------------------------------------------------------
        # Game Attributes Initialization
        self.fade_in = True
        for timer in self.timer_dict:
            self.timer_dict[timer].time_reset()

    def draw_bars(self, dt):  # Draw Health bars
        # ------------------------------------------------------------------------------------------------------------------
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.hp_player)) + "HP", white, self.config.f_hp_bar_hp, self.game_canvas,
                       self.hp_bar_player.x, self.hp_bar_player.y - self.hp_bar_player.h * 3)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.game_canvas, self.hp_bar_player.x,
                       self.hp_bar_player.y + self.hp_bar_player.h + 5)
        self.hp_bar_player.render(self.hp_player, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        draw_text_right(str(math.ceil(self.hp_boss)) + "HP", white, self.config.f_hp_bar_hp, self.game_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
        draw_text_right(self.boss_data["boss"]["name"], white, self.config.f_hp_bar_name, self.game_canvas,
                        self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 10)
        self.hp_bar_boss.render(self.hp_boss, 0.3, dt, True)

    def draw_boss(self):
        offset = 10 * math.sin(pg.time.get_ticks() / 500)
        center_blit_image(self.game_canvas, self.config.DEVIL_CHAN_face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click):
        mouse_pos = (0, 0)
        if not self.pairs:
            self.pairs = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
        if self.card_canvas_y != self.height:
            self.card_canvas.fill(white)
            if self.energy and not self.game_transition_in and not self.game_transition_out:
                self.card_complete = self.player.complete()
                if self.card_complete[0] == 2:
                    if not self.timer_dict["action"].activate_timer:
                        self.timer_dict["action"].time_start()
                    if self.timer_dict["action"].seconds > 0.25:
                        self.damage += self.card_complete[2] * 10
                        self.energy -= self.card_complete[1]
                        self.player.reset()
                        self.timer_dict["action"].time_reset()
                if click:
                    mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_cards(mouse_pos, self.card_complete[0], self.config.background, 0,
                                   self.energy and not self.timer_dict["action"].seconds > 500)
            self.game_canvas.blit(self.card_canvas, (0, self.card_canvas_y))

    def trigger_in(self):
        if not self.card_game:
            self.game_transition_in = True
            self.game_transition_out = False

    def trigger_out(self):
        if self.card_game:
            self.game_transition_in = False
            self.game_transition_out = True

    def event_handler(self, dt):
        match self.event:
            case "cinematic":
                pass
            case "dialogue":
                pass
            case "attack":
                pass
            case "death":
                pass
            case "card game":
                pass

        if self.cinematic:
            seconds = self.timer_dict["cinematic"].seconds
            clear = self.boss.opening_phrases[self.message]["clear"]
            wait = self.boss.opening_phrases[self.message]["wait"]
            if seconds > 1.5:
                self.textbox_logic(self.boss.opening_phrases, dt, clear, wait, self.boss.opening_phrases[self.message]["fade_in"],
                                   self.boss.opening_phrases[self.message]["fade_out"])
                if self.message == len(self.boss.opening_phrases):
                    self.cinematic = False
                    self.message = 0
        else:
            pass

    def textbox_logic(self, messages, dt, clear, wait, fade_in, fade_out):
        # ----------------------------------------------------------------------------------------------------------
        if self.update:  # Update these values once per message change
            self.update = False
            self.fade_in_text = fade_in
            self.fade_out_text = fade_out
        # ----------------------------------------------------------------------------------------------------------
        # Textbox Fade In
        if self.fade_in_text and not self.finished:
            if self.fade_screen_in("text", self.text_canvas, self.transition_speed, dt):
                self.fade_in_text = False
        # ----------------------------------------------------------------------------------------------------------
        # E.G. self.boss.opening_phrases -> [['Angel Chan...', 0.02, [0, 0]], ['I loved you!', 0.03, [5, 0]], ['How could you do this!?', 0.02, [20, 20]]]
        # Draw Text
        if not self.fade_in_text:
            match messages[self.message]["line"]:
                case 1:
                    self.typewriter_l1.queue_text(
                        messages[self.message]["text"])  # Method has logic inside it to only update once in a loop
                    self.finished = self.typewriter_l1.render(self.text_canvas,
                                                              messages[self.message]["delay"],
                                                              self.config.f_boss_text, white, self.align_x, self.align_y1,
                                                              messages[self.message]["shake"],
                                                              messages[self.message]["pause"], 0)
                case 2:  # Migrate the dictionary into a parameter
                    self.typewriter_l2.queue_text(
                        messages[self.message]["text"])  # Method has logic inside it to only update once in a loop
                    # Render first line
                    self.typewriter_l1.render(self.text_canvas,
                                              messages[self.message - 1]["delay"],
                                              self.config.f_boss_text, white, self.align_x, self.align_y1,
                                              messages[self.message - 1]["shake"],
                                              messages[self.message - 1]["pause"], 0)
                    # # Render second line
                    self.finished = self.typewriter_l2.render(self.text_canvas,
                                                              messages[self.message]["delay"],
                                                              self.config.f_boss_text, white, self.align_x, self.align_y2,
                                                              messages[self.message]["shake"],
                                                              messages[self.message]["pause"], 0)
        # ----------------------------------------------------------------------------------------------------------
        if self.finished:  # This occurs after the typewriter has finished blitting and completed its pause
            if self.fade_out_text:  # Fades out textbox if required
                if self.fade_screen_out("text", self.text_canvas, self.transition_speed, dt):
                    if clear:  # Clears textboxes if true & after the textbox finishes fading out
                        self.typewriter_l1.clear()
                        self.typewriter_l2.clear()
                    if self.message < len(messages) - 1:  # Transition to next message
                        self.next_msg(wait)
                        return True
            else:
                if clear:  # Clears textboxes if true (even if fade out isn't true) - Instant clear
                    self.typewriter_l1.clear()
                    self.typewriter_l2.clear()
                if self.message < len(messages) - 1:  # Transition to next message
                    self.next_msg(wait)
                    return True
        return False

    def next_msg(self, wait):
        if self.timer_dict["update_delay"].seconds < wait:
            self.timer_dict["update_delay"].time_start()
        else:
            self.timer_dict["update_delay"].time_reset()
            self.message += 1
            self.update = True
            self.finished = False
            self.typewriter_l1.unlock()
            self.typewriter_l2.unlock()

    def run(self):
        # ----------------------------------------------------------------------------------------------------------
        self.reload()
        self.timer_dict["cinematic"].time_start()
        self.typewriter_l1.time_start()
        self.typewriter_l2.time_start()
        # ----------------------------------------------------------------------------------------------------------
        # Custom Events
        milliseconds = pg.USEREVENT
        pg.time.set_timer(milliseconds, 10)
        # ----------------------------------------------------------------------------------------------------------
        # Initial parameters
        acted = True
        completed = True
        time_elapsed = Timer()
        time_elapsed.time_start()
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
                if event.type == milliseconds:
                    self.typewriter_l1.stopwatch()
                    self.typewriter_l2.stopwatch()
                    for timer in self.timer_dict:
                        self.timer_dict[timer].stopwatch()
                    time_elapsed.stopwatch()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_out and not self.freeze:
                self.transition_in("game", self.game_canvas, dt)
            elif self.freeze:  # To prevent the transition from happening offscreen
                self.freeze = False
            # ------------------------------------------------------------------------------------------------------------------
            self.fill_screens()
            self.game_canvas.blit(self.config.DEVIL_CHAN_background, (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            # Matching Game Triggers
            if self.hp_boss and self.hp_player:
                if not self.card_game and completed and not self.timer_dict["transition"].seconds:
                    self.trigger_in()
                elif self.card_game and self.energy == 0 and not self.timer_dict["transition"].seconds:
                    self.trigger_out()
            # ------------------------------------------------------------------------------------------------------------------
            if self.game_transition_in:
                if not self.timer_dict["transition"].activate_timer:
                    self.timer_dict["transition"].time_start()
                if self.card_canvas_y > 1:
                    self.card_canvas_y = move_pos(True, self.timer_dict["transition"].seconds, self.height, 25)
                elif self.card_canvas_y <= 1:
                    self.card_canvas_y = 0
                    self.game_transition_in = False
                    self.card_game = True
                    self.timer_dict["transition"].time_reset()
            # ------------------------------------------------------------------------------------------------------------------
            # Transition Out
            if self.game_transition_out:
                if not self.timer_dict["transition"].activate_timer:
                    self.timer_dict["transition"].time_start()
                if self.card_canvas_y < self.height - 1:
                    self.card_canvas_y = move_pos(False, self.timer_dict["transition"].seconds, self.height, 25)
                    self.card_game = False
                elif self.card_canvas_y >= self.height - 1:
                    self.card_canvas_y = self.height
                    self.game_transition_out = False
                    acted = False
                    completed = False
                    self.timer_dict["transition"].time_reset()
            # ------------------------------------------------------------------------------------------------------------------
            if not self.card_game:  # Don't render if the card game is fully up
                if not self.timer_dict["action"].activate_timer and not completed:
                    self.timer_dict["action"].time_start()
                if not self.timer_dict["death"].activate_timer:
                    if self.timer_dict["action"].seconds > 1:
                        self.boss.update(self.damage)
                        self.hp_boss = self.boss.health
                        self.energy = self.boss.energy
                        self.damage = 0
                    if self.timer_dict["action"].seconds > 1.5 and not acted:
                        self.boss.trigger_method()
                        action = self.boss.act()
                        if action[0] != "die":
                            self.hp_player -= action[1][0]
                        self.hp_boss = self.boss.health
                        acted = True
                    elif self.timer_dict["action"].seconds > 2:
                        self.timer_dict["action"].time_reset()
                        completed = True
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                self.draw_boss()  # Draw Boss' Image (See Method Above)
                # Textbox
                pg.draw.rect(self.text_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.text_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
                self.event_handler(dt)
                # ------------------------------------------------------------------------------------------------------------------
                if self.back_button.run(mx, my, cw_light_blue, self.click):
                    self.fade_out = True
                    self.next_level = 2
                if self.transition_out("game", self.game_canvas, dt):
                    self.restore()
                    return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.hp_player <= 0:
                if not self.timer_dict["death"].activate_timer:
                    self.timer_dict["death"].time_start()
                if self.timer_dict["death"].seconds > 1.5:
                    return 13
            elif self.hp_boss <= 0:
                if not self.timer_dict["death"].activate_timer:
                    self.timer_dict["death"].time_start()
                if self.timer_dict["death"].seconds > 1.5:
                    return 14
            # ------------------------------------------------------------------------------------------------------------------
            if self.hp_boss and self.hp_player:
                self.run_card_game(self.click)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens(self.card_canvas, 0, self.card_canvas_y)
            self.clock.tick(self.FPS)
            pg.display.update()
