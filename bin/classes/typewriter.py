import os
import random

import pygame as pg

from stopwatch import Timer


class Typewriter(Timer):
    def __init__(self, surface, audio):
        super().__init__()  # Inherit Timer Class
        self.surface = surface
        self.string = []
        self.blitted_string = ""
        self.text = ""
        self.length = 0
        self.audio = audio
        # self.boop = pg.mixer.Sound(os.getcwd() + "/resources/audio/boop/boop.wav")
        # self.boops_directory = os.getcwd() + "/resources/audio/boops"
        # self.boops = load_audio_set(self.boops_directory, ".wav")  # Load Music Into a List

    def update_string(self, s):
        self.string = list(s)

    def update_text(self, delay, boop_type):
        if self.seconds >= delay:  # Creates controlled "delay" in seconds
            try:
                letter = self.string.pop(0)
                self.blitted_string += letter  # Add letter in first element
                if letter != " ":
                    if boop_type == 0:  # Normal boop sound
                        if not pg.mixer.Channel(4).get_busy():
                            self.audio.channel4.play(self.boop)
                    if boop_type == 1:  # Variations of the boop sound
                        if not pg.mixer.Channel(4).get_busy():
                            idx = random.randint(0, len(os.listdir(self.boops_directory)))
                            self.audio.channel4.play(self.boops[idx])
            except IndexError:
                pass
            self.seconds = 0  # Reset timer

    def render_font(self, font, clr):
        self.text = font.render(self.blitted_string, True, clr)

    def draw_font(self, delay, font, clr, x, y, boop_type):
        self.update_text(delay, boop_type)
        self.render_font(font, clr)
        self.surface.blit(self.text, (x, y))
