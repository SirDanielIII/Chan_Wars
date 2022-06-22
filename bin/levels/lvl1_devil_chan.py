import math
import random
import time

import bin.levels.minigames.card_game.player as card_pair
from bin.blit_tools import draw_text_left, draw_text_right, draw_rect_outline, center_blit_image
from bin.classes.buttons import ButtonTriangle
from bin.classes.entities.bosses import DevilChan
from bin.classes.entities.enemy import Enemy
from bin.classes.health_bar import HealthBar
from bin.classes.level import Level
from bin.classes.queue import Queue
from bin.classes.stopwatch import Timer
from bin.classes.typewriter import Typewriter
from bin.colours import *
from bin.levels.minigames.card_game.player import move_pos


class BossDevilChan(Level):
    def __init__(self, width, height, surface, game_canvas, clock, last_time, config, audio):
        super().__init__(width, height, surface, game_canvas, clock, last_time, config, audio)
        self.back_button = ButtonTriangle(self.game_canvas, cw_blue)
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
        self.card_match = [0]
        self.size = None
        # ------------------------------------------------------------------------------------------------------------------
        # Enemy Attributes
        self.hp_enemy_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_bar_enemy = None
        self.enemy_name = None
        self.enemy = Enemy(None)
        self.enemy_face = None
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Attributes
        self.hp_boss_rect = pg.Rect(1170, 545, 330, 35)
        self.hp_bar_boss = None
        self.boss_name = "devil_chan"
        self.boss = DevilChan(None)
        self.boss_face = None
        # ------------------------------------------------------------------------------------------------------------------
        # Battle Attributes
        self.level = 1
        self.turn_counter = None
        self.completed = True
        self.battle = "enemy"
        self.updated = True
        self.acted = True
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
        # Event Handler
        self.event = "enemy_intro"
        # ------------------------------------------------------------------------------------------------------------------
        # Timer Attributes
        self.timer_dict = {"action": Timer(), "card": Timer(), "dialogue": Timer(), "transition": Timer(), "update_delay": Timer(), "update": Timer()}

    def reload(self):  # Sets generic values here. Run every time a new fight is initiated.
        # ------------------------------------------------------------------------------------------------------------------
        # Generic Attributes
        self.turn_counter = 0
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

    def initialize_player(self):    # Run once at the start of the level. Player attributes are not reset between every battle.
        # ------------------------------------------------------------------------------------------------------------------
        # Player Attributes Initialization
        self.player.metadata = self.config.level_confs[self.level]["player"]
        self.player.initialize(self.config.img_cards)
        self.player.image_list = self.config.img_cards
        self.hp_bar_player = HealthBar(self.game_canvas, self.hp_player_rect, self.player.health, cw_green, white, 5, True, cw_dark_red, True,
                                       cw_yellow)
        self.size = self.config.chan_card_size

    def initialize_boss(self):    # Run once at the start of the level.
        # ------------------------------------------------------------------------------------------------------------------aal
        # Boss Attributes Initialization
        self.boss.metadata = self.config.boss_confs[self.boss_name]
        self.boss.initialize()
        self.hp_bar_boss = HealthBar(self.game_canvas, self.hp_boss_rect, self.boss.health, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.boss_face = self.config.img_bosses[self.level]

    def initialize_enemy(self):    # Run once at the start of the level. This method is run again for every enemy battle.
        # ------------------------------------------------------------------------------------------------------------------
        # Enemy Attributes Initialization
        self.enemy_name = "goblin"      # random.choice(list(self.config.level_confs[self.level]["enemies"].keys())[:-1])
        self.enemy.metadata = self.config.level_confs[self.level]["enemies"][self.enemy_name]
        self.enemy.initialize(self.enemy_name, self.config.level_confs[self.level]["enemies"]["phrases"])
        self.hp_bar_enemy = HealthBar(self.game_canvas, self.hp_enemy_rect, self.enemy.health, cw_green, white, 5, True, cw_dark_red, True, cw_yellow)
        self.enemy_face = self.config.img_enemies[self.enemy_name]

    def battle_reset(self):
        self.player.played_cards = None
        self.player.debuff_bar = {"fear": 0, "weakness": 0, "vulnerable": 0, "disappointment": 0, "wounded": 0, "marked": 0}
        self.player.buff_bar = {"power": 0, "lifesteal": 0, "regeneration": 0, "energized": 0, "armor": 0, "clairvoyant": 0}
        self.player.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}}
        self.player.chosen_cards = []
        self.player.energy = self.player.metadata["energy"]
        self.turn_counter = 0
        self.completed = True
        self.updated = True
        self.acted = True
        for timer in self.timer_dict:
            self.timer_dict[timer].time_reset()

    def draw_bars(self, dt):  # Draw Health bars
        # ------------------------------------------------------------------------------------------------------------------
        # Player Text & Health Bar
        draw_text_left(str(math.ceil(self.player.health)) + "HP", white, self.config.f_hp_bar_hp, self.game_canvas,
                       self.hp_bar_player.x, self.hp_bar_player.y - self.hp_bar_player.h * 3)
        draw_text_left("You", white, self.config.f_hp_bar_name, self.game_canvas, self.hp_bar_player.x,
                       self.hp_bar_player.y + self.hp_bar_player.h + 5)
        self.hp_bar_player.render(self.player.health, 0.3, dt)
        # ------------------------------------------------------------------------------------------------------------------
        # Boss Text & Health Bar
        if self.battle == "boss":
            draw_text_right(str(math.ceil(self.boss.health)) + "HP", white, self.config.f_hp_bar_hp, self.game_canvas,
                            self.hp_bar_boss.x + self.hp_bar_boss.w + 10, self.hp_bar_boss.y)
            draw_text_right(self.boss.metadata["name"], white, self.config.f_hp_bar_name, self.game_canvas,
                            self.hp_bar_boss.x + self.hp_bar_boss.w + 5, self.hp_bar_boss.y + self.hp_bar_boss.h * 2 + 10)
            self.hp_bar_boss.render(self.boss.health, 0.3, dt, True)
        # ------------------------------------------------------------------------------------------------------------------
        # Enemy Text & Health Bar
        if self.battle == "enemy":
            draw_text_right(str(math.ceil(self.enemy.health)) + "HP", white, self.config.f_hp_bar_hp, self.game_canvas,
                            self.hp_bar_enemy.x + self.hp_bar_enemy.w + 10, self.hp_bar_enemy.y)
            draw_text_right(self.enemy.metadata["name"], white, self.config.f_hp_bar_name, self.game_canvas,
                            self.hp_bar_enemy.x + self.hp_bar_enemy.w + 5, self.hp_bar_enemy.y + self.hp_bar_enemy.h * 2 + 10)
            self.hp_bar_enemy.render(self.enemy.health, 0.3, dt, True)

    def draw_boss(self):
        # ------------------------------------------------------------------------------------------------------------------
        # Draws the Boss
        offset = 10 * math.sin(pg.time.get_ticks() / 500)
        center_blit_image(self.game_canvas, self.boss_face, self.width / 2, self.height / 2 - 100 + offset)

    def draw_enemy(self):
        # ------------------------------------------------------------------------------------------------------------------
        # Draws the Enemy
        offset = 10 * math.sin(pg.time.get_ticks() / 500)
        center_blit_image(self.game_canvas, self.enemy_face, self.width / 2, self.height / 2 - 100 + offset)

    def run_card_game(self, click):
        mouse_pos = (0, 0)
        if self.card_canvas_y != self.height:   # Makes sure that the card game is only run while teh screen is up.
            if not self.player.played_cards:    # Generates a new set of cards if no cards already exist.
                self.player.played_cards = self.player.generate_pairs(self.size, self.margins, self.width, self.height)
            self.card_canvas.fill((255, 255, 255))
            # ------------------------------------------------------------------------------------------------------------------
            if self.player.energy and not self.game_transition_in and not self.game_transition_out:
                if self.card_match[0] != 2:     # If a match hasn't been made, allow teh player to continue trying to match.
                    self.card_match = self.player.complete()
                # ------------------------------------------------------------------------------------------------------------------
                # Completes the card matching process
                if self.card_match[0] == 2:
                    if not self.timer_dict["card"].activate_timer:
                        self.timer_dict["card"].time_start()
                    if self.timer_dict["card"].seconds > 0.25:  # Completes the match by reducing the player's energy
                        self.player.energy -= 1
                        self.player.reset()
                        self.timer_dict["card"].time_reset()
                        self.card_match = self.player.complete()
                if click:
                    mouse_pos = tuple(pg.mouse.get_pos())
            self.player.draw_card_screen(self.config.f_status, self.config.f_intro, self.config.f_stats, self.config.img_ui, mouse_pos, self.card_match[0], self.config.img_levels["Card_Game"],
                                         0, self.player.energy and not self.timer_dict["card"].seconds > 500 and not self.game_transition_in and not self.game_transition_out, self.audio, self.config.audio_interact["click"])
            # Draws the cards and creates matches between clicked cards.

    def trigger_in(self):   # Called to bring the card game back in.
        if not self.card_game:
            self.game_transition_in = True
            self.game_transition_out = False

    def trigger_out(self):  # Called to transition out of the card game.
        if self.card_game:
            self.game_transition_in = False
            self.game_transition_out = True

    def event_handler(self, dt):
        match self.event:
            # ------------------------------------------------------------------------------------------------------------------
            # Generic Events
            case "attack":  # Event happens after dialogue is complete. Brings up the card game screen.
                self.attack()
            # ------------------------------------------------------------------------------------------------------------------
            # Boss events
            case "boss_intro":  # Event happens when the boss fight is initiated. Introduction dialogue is initiated.
                self.typewriter_queue("boss_intro", "multiple")
                self.dialogue(1.0, dt)
            case "boss_special":    # Event happens when the boss uses its special move. Special attack dialogue is initiated.
                self.typewriter_queue("boss_special", "random")
                self.dialogue(1.0, dt)
            case "boss_basic":  # Event happens when the boss uses its basic move. Basic attack dialogue is initiated.
                self.typewriter_queue("boss_basic", "random")
                self.dialogue(1.0, dt)
            case "boss_death":  # Event happens when the boss is defeated. Boss death dialogue is initiated.
                self.typewriter_queue("boss_death", "multiple")
                self.dialogue(1.0, dt)
            case "boss_player_death":   # Event happens when the player dies while fighting the boss. Boss' winning dialogue is initiated.
                self.typewriter_queue("boss_player_death", "multiple")
                self.dialogue(1.0, dt)
            # ------------------------------------------------------------------------------------------------------------------
            # Enemy events
            case "enemy_intro":     # Event happens when the enemy fight is initiated. Introduction dialogue is initiated.
                self.typewriter_queue("enemy_intro")
                self.dialogue(1.0, dt)
            case "enemy_basic":     # Event happens when the enemy uses its basic move. Basic attack dialogue is initiated.
                self.typewriter_queue("enemy_basic")
                self.dialogue(1.0, dt)
            case "enemy_death":     # Event happens when the enemy is defeated. Enemy death dialogue is initiated.
                self.typewriter_queue("enemy_death")
                self.dialogue(1.0, dt)
            case "enemy_player_death":  # Event happens when the player dies while fighting an enemy. Enemy winning dialogue is initiated.
                self.typewriter_queue("enemy_player_death", "multiple")
                self.dialogue(1.0, dt)
        # print(f"Event: {self.event}\tMessage Line: {self.typ_msg}\tLength of Messages: {len(self.boss.phrases['intro'])}")

    def typewriter_queue(self, e, quote_type=None):
        if self.typ_queue_update:  # Only runs once
            self.typ_queue_update = False
            self.timer_dict["dialogue"].time_start()
            # ------------------------------------------------------------------------------------------------------------------
            # Dialogue for boss events
            if "boss" in e:
                if quote_type == "multiple":    # If there are multiple lines, queues all of them in order.
                    for key in self.boss.phrases[e]:
                        self.typ_queue.enqueue(self.boss.phrases[e][key])
                elif quote_type == "random":    # If there are several versions of a line, and one is chosen randomly, queues a random line.
                    self.typ_queue.enqueue(self.boss.phrases[e][random.randint(0, len(self.boss.phrases[e]) - 1)])
                else:   # If there is only one version of the dialogue, and it is only one line, queues the line
                    self.typ_queue.enqueue(self.boss.phrases[e])
            # ------------------------------------------------------------------------------------------------------------------
            # Dialogue for enemy events
            if "enemy" in e:
                if quote_type == "multiple":    # If there are multiple lines, queues all of them in order.
                    for key in self.enemy.phrases[e]:
                        self.typ_queue.enqueue(self.enemy.phrases[e][key])  # Queue all messages in order
                elif quote_type == "random":    # If there are several versions of a line, and one is chosen randomly, queues a random line.
                    self.typ_queue.enqueue(self.enemy.phrases[e][random.randint(0, len(self.enemy.phrases[e]) - 1)])
                else:   # If there is only one version of the dialogue, and it is only one line, queues the line
                    self.typ_queue.enqueue(self.enemy.phrases[e])
        # print(self.typ_queue.items)

    def dialogue(self, delay, dt):
        seconds = self.timer_dict["dialogue"].seconds
        if seconds > delay:     # Implements delay before the message is blit onto the screen.
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
        if self.boss.health:
            if not self.card_game and self.completed and not self.timer_dict["transition"].seconds:
                self.trigger_in()
            elif self.card_game and self.player.health != 0 and not self.timer_dict["transition"].seconds and not self.player.energy:
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
        # Initializes the generic attributes, teh player attributes, the boss attributes and teh enemy attributes.
        self.reload()
        self.initialize_player()
        self.initialize_enemy()
        self.initialize_boss()
        enemy_count = 0
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
                    self.config.shutdown(self.config.global_conf)
                if event.type == pg.MOUSEBUTTONDOWN:  # When Mouse Button Clicked
                    if event.button == 1:  # Left Mouse Button
                        self.click = True
                if event.type == milliseconds:  # Timers
                    self.typ_l1.stopwatch()
                    self.typ_l2.stopwatch()
                    for timer in self.timer_dict:  # Loop through timers and run them
                        self.timer_dict[timer].stopwatch()  # If `self.activate_timer = False` then this won't update
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
                if not self.timer_dict["update"].activate_timer and not self.updated and not self.completed:
                    self.timer_dict["update"].time_start()
                if not self.timer_dict["action"].activate_timer and not self.completed:
                    self.timer_dict["action"].time_start()
                # ------------------------------------------------------------------------------------------------------------------
                if self.timer_dict["update"].seconds > 1:
                    # Updates the state of the opponent. self.battle determines whether the boss or enemy is being fought
                    if self.battle == "boss":
                        self.boss.update(self.player.attack["damage"], self.player.attack["debuff"])
                        if self.player.attack["damage"] > self.boss.block:
                            self.audio.dj(None, None, None, 800, False, 3, self.config.audio_game["hit"])
                    elif self.battle == "enemy":
                        self.enemy.update(self.player.attack["damage"], self.player.attack["debuff"])
                        if self.player.attack["damage"] > self.enemy.block:
                            self.audio.dj(None, None, None, 800, False, 3, self.config.audio_game["hit"])
                    self.updated = True
                    self.timer_dict["update"].time_reset()
                # ------------------------------------------------------------------------------------------------------------------
                if self.timer_dict["action"].seconds > 2 and not self.acted and "death" not in self.event:
                    # Makes the opponent act.
                    if self.battle == "boss":
                        phrase = self.boss.act(self.turn_counter)
                        if "basic" in phrase:
                            self.event = "boss_basic"
                        elif "special" in phrase:
                            self.event = "boss_special"
                    elif self.battle == "enemy":
                        self.enemy.act(self.turn_counter)
                        self.event = "enemy_basic"
                    self.acted = True
                # ------------------------------------------------------------------------------------------------------------------
                elif self.timer_dict["action"].seconds > 3 and "death" not in self.event:
                    # Completes the process, updates the player's state and puts the dialogue on screen.
                    if self.battle == "boss":
                        self.player.update(self.boss.move["damage"], self.boss.move["debuff"])
                        if self.boss.move["damage"] > self.player.block:
                            self.audio.dj(None, None, None, 800, False, 1, self.config.audio_game["attack"])
                        self.boss.move = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}}
                    elif self.battle == "enemy":
                        self.player.update(self.enemy.attack["damage"], self.enemy.attack["debuff"])
                        if self.enemy.attack["damage"] > self.player.block:
                            self.audio.dj(None, None, None, 800, False, 1, self.config.audio_game["attack"])
                        self.enemy.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}}
                    self.player.attack = {"damage": 0, "block": 0, "heal": 0, "buff": {}, "debuff": {}}
                    self.turn_counter += 1
                    self.timer_dict["action"].time_reset()
                    self.completed = True
                # ------------------------------------------------------------------------------------------------------------------
                self.draw_bars(dt)  # Draw Health Bars (See Method Above)
                if self.battle == "boss":
                    self.draw_boss()  # Draw Boss' Image (See Method Above)
                if self.battle == "enemy":
                    self.draw_enemy()  # Draw Enemy's Image (See Method Above)
                # Textbox
                pg.draw.rect(self.text_canvas, cw_dark_grey, pg.Rect(95, 650, self.width - 95 * 2, 175))
                draw_rect_outline(self.text_canvas, white, pg.Rect(95, 650, self.width - 95 * 2, 175), 10)
                # ------------------------------------------------------------------------------------------------------------------
                if self.back_button.run(mx, my, cw_light_blue, self.click):
                    self.fade_out = True
                    self.next_level = 2
                    self.audio.dj(None, None, None, 800, False, 0, self.config.audio_interact["click"])
                    self.audio.dj(None, None, None, 800, False, 1, self.config.audio_interact["fade"])
                if self.back_button.check_hover():
                    self.audio.dj(None, None, None, 800, False, 2, self.config.audio_interact["highlight"])
                    self.next_level = 2
                if self.transition_out("game", self.game_canvas, dt):
                    self.restore()
                    return self.next_level
            # ------------------------------------------------------------------------------------------------------------------
            if self.typ_queue.is_empty():
                if "death" in self.event and "boss" in self.event or "player" in self.event:  # Finishes the level if the boss is killed.
                    return 8 if self.player.health <= 0 else 9
                elif "death" in self.event and "enemy" in self.event:   # Resets the battle state and brings up a new enemy if an enemy dies
                    enemy_count += 1
                    if enemy_count != 3:
                        self.battle_reset()
                        self.initialize_enemy()
                        self.event = "enemy_intro"
                    else:
                        self.battle_reset()
                        self.battle = "boss"
                        self.event = "boss_intro"
                        self.audio.dj(None, None, None, 800, False, 3, self.config.audio_game["introduce_boss"])
                if self.player.health <= 0 and self.battle == "boss":
                    self.event = "boss_player_death"
                    self.audio.dj(None, None, None, 800, False, 2, self.config.audio_game["player_death"])
                elif self.boss.health <= 0 and self.battle == "boss":
                    self.event = "boss_death"
                if self.player.health <= 0 and self.battle == "enemy":
                    self.event = "enemy_player_death"
                    self.audio.dj(None, None, None, 800, False, 2, self.config.audio_game["player_death"])
                elif self.enemy.health <= 0 and self.battle == "enemy":
                    self.event = "enemy_death"
                    self.audio.dj(None, None, None, 800, False, 2, self.config.audio_game["enemy_death"])
            # ------------------------------------------------------------------------------------------------------------------
            if not self.fade_in:  # Run event logic after screen transition in and not during attack phase
                self.event_handler(dt)
            # ------------------------------------------------------------------------------------------------------------------
            if ((self.boss.health and self.battle == "boss") or (self.enemy.health and self.battle == "enemy")) and self.player.health:
                self.run_card_game(self.click)
            # ------------------------------------------------------------------------------------------------------------------
            self.blit_screens([[self.card_canvas, (0, self.card_canvas_y)]])
            self.clock.tick(self.config.FPS)
            self.audio.audio_mixer()
            pg.display.update()
