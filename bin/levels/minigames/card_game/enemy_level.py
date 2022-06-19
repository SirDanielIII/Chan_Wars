import math
import random
import sys
import time

import bin.levels.minigames.card_game.player as card_pair
from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.entities.enemy import Enemy
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.classes.queue import Queue
from bin.classes.stopwatch import Timer
from bin.classes.typewriter import Typewriter
from bin.colours import *


class EnemyLevel(Level):
    def __init__(self, width, height, surface, game_canvas, clock, fps, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, fps, last_time, config, audio)
        self.audio = audio
        self.back_button = ButtonTriangle(self.text_canvas, cw_blue)
        # ------------------------------------------------------------------------------------------------------------------
        # Card Game Attributes
        self.card_canvas = pg.Surface((self.width, self.height), flags=pg.HWACCEL and pg.DOUBLEBUF and pg.SRCALPHA).convert_alpha()
        self.card_canvas_y = self.height
        self.card_game = False
        self.game_transition_in = False
        self.game_transition_out = False  # Use this to stop the game
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes
        self.hp_player_rect = pg.Rect(100, 545, 330, 35)
        self.hp_bar_player = None
        self.player = card_pair.Player(self.card_canvas, None)
        self.margins = (20, 30)
        self.card_complete = [0]
        self.size = None
        # ------------------------------------------------------------------------------------------------------------------
        # Enemy Attributes
        self.hp_enemy_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_bar_enemy = None
        self.acted = True
        self.completed = True
        self.updated = True
        self.name = None
        self.level = None
        self.turn_counter = None
        self.enemy = Enemy(None)
        self.face = None
        # ------------------------------------------------------------------------------------------------------------------
        # Text Bar Attributes
        self.typ_transition_in = False
        self.typ_transition_out = False
        self.typ_l1 = Typewriter()
        self.typ_l2 = Typewriter()
        self.typ_finished = False
        self.typ_update = True
        self.typ_box_align_x = 130
        self.typ_box_align_y1 = 670
        self.typ_box_align_y2 = 730
        self.typ_queue = Queue()
        self.typ_queue_update = True
        self.typ_last_shake = [0, 0]
        # ------------------------------------------------------------------------------------------------------------------
        self.timer_dict = {"action": Timer(), "card": Timer(), "dialogue": Timer(), "transition": Timer(), "update_delay": Timer()}
        self.event = "intro"

    def reload(self):  # Set values here b/c `self.config = None` when the class is first initialized
        self.level = 1
        self.turn_counter = 0
        config = self.config.get_config("level")
        self.name = random.choice(list(config[self.level]["enemies"].keys())[:-1])
        self.player.metadata = config[self.level]["player"]
        self.enemy.metadata = config[self.level]["enemies"][self.name]
        self.enemy.initialize(self.name, config[self.level]["enemies"]["phrases"])
        self.player.initialize(self.config.img_cards)
        self.player.image_list = self.config.img_cards
        self.size = self.config.chan_card_size
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.player.health, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.hp_bar_enemy = HealthBar(self.game_canvas, self.hp_enemy_rect, self.enemy.health, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.face = self.config.img_enemies[self.name]
        # ------------------------------------------------------------------------------------------------------------------
        # Text Box & Typewriter Attributes
        self.typ_transition_in = False
        self.typ_l1 = Typewriter()
        self.typ_l2 = Typewriter()
        self.typ_finished = False
        self.typ_update = True
        self.typ_box_align_x = 130
        self.typ_box_align_y1 = 670
        self.typ_box_align_y2 = 730
        self.typ_queue = Queue()
        self.typ_queue_update = True
        self.typ_last_shake = [0, 0]
        # ------------------------------------------------------------------------------------------------------------------
        # Game Attributes Initialization
        self.fade_in = True
        for timer in self.timer_dict:
            self.timer_dict[timer].time_reset()

    def draw_bars(self, dt):  # Draw Health bars
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.player.health)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.text_canvas, self.hp_bar_player.x, self.hp_bar_player.y + self.hp_bar_player.h * 2 + 5)
        self.hp_bar_player.render(self.player.health, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Enemy Text & Health Bar
        draw_text_right(str(math.ceil(self.enemy.health)) + "HP", white, self.config.f_hp_bar_hp, self.text_canvas,
                        self.hp_bar_enemy.x + self.hp_bar_enemy.w + 10, self.hp_bar_enemy.y)
        draw_text_right(self.enemy.name, white, self.config.f_hp_bar_name, self.text_canvas,
                        self.hp_bar_enemy.x + self.hp_bar_enemy.w + 5, self.hp_bar_enemy.y + self.hp_bar_enemy.h * 2 + 5)
        self.hp_bar_enemy.render(self.enemy.health, 0.3, dt, True)

    def draw_enemy(self):
        offset = 10 * math.sin(pg.time.get_ticks() / 500)  # VELOCITY FUNCTION HERE (SLOPE)
        center_blit_image(self.game_canvas, self.face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click):
        mouse_pos = (0, 0)
        if self.card_canvas_y != self.height:
            if not self.player.played_cards:
                self.player.played_cards = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
            self.card_canvas.fill((255, 255, 255))
            # ------------------------------------------------------------------------------------------------------------------
            if self.player.energy and not self.game_transition_in and not self.game_transition_out:
                # This if statement prevents you from changing the state of the cards while the screen is moving or you don't have enough energy - Daniel
                if self.card_complete[0] != 2:
                    self.card_complete = self.player.complete()
                if self.card_complete[0] == 2:
                    if not self.timer_dict["card"].activate_timer:
                        self.timer_dict["card"].time_start()
                    if self.timer_dict["card"].seconds > 0.25:
                        self.player.energy -= 1
                        self.player.reset()
                        self.timer_dict["card"].time_reset()
                        self.card_complete = self.player.complete()
                if click:
                    mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_card_screen(mouse_pos, self.card_complete[0], self.config.img_levels["Card_Game"], 0,
                                         self.player.energy and not self.timer_dict["card"].seconds > 500 and not self.game_transition_in and not self.game_transition_out)
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
            case "intro":
                self.typewriter_queue("intro")
                self.dialogue(1.0, dt)
            case "attack":
                self.attack()
            case "basic":
                self.typewriter_queue("basic")
                self.dialogue(1.0, dt)
            case "enemy_death":
                self.typewriter_queue("enemy_death")
                self.dialogue(1.0, dt)
            case "player_death":
                self.typewriter_queue("player_death")
                self.dialogue(1.0, dt)
        # print(f"Event: {self.event}\tMessage Line: {self.typ_msg}\tLength of Messages: {len(self.boss.phrases['intro'])}")

    def typewriter_queue(self, e):
        if self.typ_queue_update:  # Only runs once
            self.typ_queue_update = False
            self.timer_dict["dialogue"].time_start()
            match e:
                case "intro":
                    self.typ_queue.enqueue(self.enemy.phrases[e])  # Queue all messages in order
                case "basic":
                    self.typ_queue.enqueue(self.enemy.attack["phrase"])  # Choose random message
                case "enemy_death":
                    self.typ_queue.enqueue(self.enemy.phrases[e])
                case "player_death":
                    for key in self.enemy.phrases[e]:
                        self.typ_queue.enqueue(self.enemy.phrases[e][key])
        # print(self.typ_queue.items)

    def dialogue(self, delay, dt):
        seconds = self.timer_dict["dialogue"].seconds
        if seconds > delay:
            if not self.typ_queue.is_empty():
                clear = self.typ_queue.peek()["clear"]
                wait = self.typ_queue.peek()["wait"]
                self.typewriter_render(self.typ_queue, dt, clear, wait, self.typ_queue.peek()["fade_in"], self.typ_queue.peek()["fade_out"])
            if self.typ_queue.is_empty():
                if "death" not in self.event:
                    self.event = "attack"
                self.timer_dict["dialogue"].time_reset()
                self.typ_queue_update = True
                self.typ_update = True

    def attack(self):
        # ------------------------------------------------------------------------------------------------------------------
        # Matching Game Triggers
        if self.enemy.health:
            if not self.card_game and self.completed and not self.timer_dict["transition"].seconds:
                self.trigger_in()
            elif self.card_game and self.player.health != 0 and not self.timer_dict["transition"].seconds and not self.player.energy:
                self.trigger_out()
        # ------------------------------------------------------------------------------------------------------------------
        if self.game_transition_in:
            if not self.timer_dict["transition"].activate_timer:
                self.timer_dict["transition"].time_start()
            if self.card_canvas_y > 1:
                self.card_canvas_y = card_pair.move_pos(True, self.timer_dict["transition"].seconds, self.height, 25)
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
                self.card_canvas_y = card_pair.move_pos(False, self.timer_dict["transition"].seconds, self.height, 25)
                self.card_game = False
            elif self.card_canvas_y >= self.height - 1:
                self.card_canvas_y = self.height
                self.game_transition_out = False
                self.acted = False
                self.updated = False
                self.completed = False
                self.timer_dict["transition"].time_reset()

    def typewriter_render(self, messages, dt, clear, wait, fade_in, fade_out):
        if self.typ_update:  # Update these values once per message update
            self.typ_update = False
            self.fade_in_text = fade_in
            self.fade_out_text = fade_out
        # ----------------------------------------------------------------------------------------------------------
        # Textbox Fade In
        if self.fade_in_text and not self.typ_finished:  # Fade in textbox if specified
            if self.fade_screen_in("text", self.text_canvas, self.transition_speed, dt):
                self.fade_in_text = False
        # ----------------------------------------------------------------------------------------------------------
        # Draw Text
        if not self.fade_in_text:  # Run when textbox is not fading in
            match messages.peek()["line"]:
                case 1:  # Line 1
                    self.typ_l1.queue_text(messages.peek()["text"])  # Method has logic inside it to only update once in a loop
                    self.typ_finished = \
                        self.typ_l1.render(self.text_canvas,
                                           messages.peek()["delay"],
                                           self.config.f_boss_text, white, self.typ_box_align_x, self.typ_box_align_y1,
                                           messages.peek()["shake"],
                                           messages.peek()["pause"], 0)
                case 2:  # Line 2
                    self.typ_l2.queue_text(messages.peek()["text"])  # Method has logic inside it to only update once in a loop
                    # Render first line
                    if messages.size() > 1:  # Need to check this as messages gets popped when its finished blitting below
                        self.typ_l1.render(self.text_canvas,
                                           0,
                                           self.config.f_boss_text, white, self.typ_box_align_x, self.typ_box_align_y1,
                                           self.typ_last_shake,
                                           0, 0)
                    # # Render second line
                    self.typ_finished = \
                        self.typ_l2.render(self.text_canvas,
                                           messages.peek()["delay"],
                                           self.config.f_boss_text, white, self.typ_box_align_x, self.typ_box_align_y2,
                                           messages.peek()["shake"],
                                           messages.peek()["pause"], 0)
        # ----------------------------------------------------------------------------------------------------------
        if self.typ_finished:  # This occurs after the typewriter has finished blitting and completed its pause
            self.typ_last_shake = messages.peek()["shake"]  # Store last shake variable for the first line when blitting the second line
            if self.fade_out_text:  # Fades out textbox if required
                if self.fade_screen_out("text", self.text_canvas, self.transition_speed, dt):
                    if clear:  # Clears textbox if true & after the textbox finishes fading out
                        self.typ_l1.clear()
                        self.typ_l2.clear()
                        self.next_msg(wait)
            else:
                if clear:  # Clears textbox if true (even if fade out isn't true) - Instant clear
                    self.typ_l1.clear()
                    self.typ_l2.clear()
                self.next_msg(wait)

    def next_msg(self, wait):
        if self.timer_dict["update_delay"].seconds < wait:  # Seconds is initially at 0
            self.timer_dict["update_delay"].time_start()  # Start counting seconds if smaller than wait
        else:  # Reset values after delay
            self.timer_dict["update_delay"].time_reset()  # Reset delay timer
            self.typ_update = True  # Update message dictionary next loop
            self.typ_finished = False
            self.typ_l1.unlock()
            self.typ_l2.unlock()
            self.typ_queue.dequeue()  # Pop last element (dictionary) in lst

    def run(self):
        # ----------------------------------------------------------------------------------------------------------
        self.reload()
        self.timer_dict["dialogue"].time_start()
        self.typ_l1.time_start()
        self.typ_l2.time_start()
        # ----------------------------------------------------------------------------------------------------------
        # Custom Events
        milliseconds = pg.USEREVENT
        pg.time.set_timer(milliseconds, 10)
        # ----------------------------------------------------------------------------------------------------------
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
                    self.typ_l1.stopwatch()
                    self.typ_l2.stopwatch()
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
            self.game_canvas.blit(self.config.img_levels[self.level], (0, 0))
            # ------------------------------------------------------------------------------------------------------------------
            if not self.card_game:  # Don't render if the card game is fully up
                if not self.timer_dict["update_delay"].activate_timer and not self.updated and not self.completed:
                    self.timer_dict["update_delay"].time_start()
                if not self.timer_dict["action"].activate_timer and not self.completed:
                    self.timer_dict["action"].time_start()
                if self.timer_dict["update_delay"].seconds > 1.5:
                    self.enemy.update(self.player.attack["damage"], self.player.attack["status"])
                    self.updated = True
                    self.timer_dict["update_delay"].time_reset()
                if self.timer_dict["action"].seconds > 2.5 and not self.acted and "death" not in self.event:
                    self.enemy.act(self.turn_counter)
                    self.event = "basic"
                    self.acted = True
                elif self.timer_dict["action"].seconds > 4 and "death" not in self.event:
                    self.player.update(self.enemy.attack["damage"], self.enemy.attack["status"])
                    self.player.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}}
                    self.enemy.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "status": {}}
                    self.turn_counter += 1
                    self.timer_dict["action"].time_reset()
                    self.completed = True
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                self.draw_enemy(time_elapsed)  # Draw Enemy' Image (See Method Above)
                # Textbox
                pg.draw.rect(self.game_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.game_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
                # ------------------------------------------------------------------------------------------------------------------
                if self.back_button.run(mx, my, cw_light_blue, self.click):
                    self.fade_out = True
                    self.next_level = 2
                if self.transition_out("game", self.game_canvas, dt):
                    self.restore()
                    return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.typ_queue.is_empty():
                if "death" in self.event:
                    return 13 if self.player.health <= 0 else 14
                if self.player.health <= 0:
                    self.event = "player_death"
                elif self.enemy.health <= 0:
                    self.event = "enemy_death"
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_in:  # Run event logic after screen transition in and not during attack phase
                self.event_handler(dt)
            # ------------------------------------------------------------------------------------------------------------------
            if self.enemy.health and self.player.health:
                self.run_card_game(self.click)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens()
            self.clock.tick(self.FPS)
            pg.display.update()
            # print(self.clock.get_fps(), self.card_game, self.card_canvas_y, self.game_transition_in, self.game_transition_out)
