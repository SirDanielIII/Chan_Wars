from random import uniform

import pygame as pg

from .stopwatch import Timer

pg.init()


class Typewriter(Timer):  # Implementation of Queue data type / structure
    """
    This typewriter class is based off a delay in milliseconds
    You must create this custom event and run self.stopwatch() in it
    >>> milliseconds = pg.USEREVENT
    >>> pg.time.set_timer(milliseconds, 10)
    """

    def __init__(self):
        super().__init__()
        self.queue = []
        self.update_text_lock = False
        self.str_to_blit = ""
        self.blit_final = ""

    def enqueue(self, item):
        """ Adds a new item to the back of the queue.
           It needs the item and returns nothing. """
        self.queue.insert(0, item)

    def dequeue(self):
        """ Removes the top item from the queue (last index)
           It needs no parameters and returns the item. The queue is modified."""
        return self.queue.pop()

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def clear(self):
        self.queue = []
        self.str_to_blit = ""
        self.blit_final = ""

    def queue_text(self, lst):
        if not self.update_text_lock:
            for i in lst:
                self.enqueue(i)
        self.update_text_lock = True

    def unlock(self):
        self.update_text_lock = False

    def render(self, screen, delay, font, clr, x, y, shake, pause, boop_type):
        self.blit_final = font.render(self.str_to_blit, True, clr)
        screen.blit(self.blit_final, (x + uniform(0, shake[0]), y + uniform(0, shake[1])))
        # Typewriter Effect
        if not self.is_empty() and self.seconds >= delay:  # Creates controlled "delay" in seconds
            try:
                letter = self.dequeue()
                self.str_to_blit += letter
                if letter != " ":
                    # if boop_type == 0:  # Normal boop sound
                    #     if not pg.mixer.Channel(4).get_busy():
                    #         self.audio.channel4.play(self.boop)
                    # if boop_type == 1:  # Variations of the boop sound
                    #     if not pg.mixer.Channel(4).get_busy():
                    #         idx = random.randint(0, len(os.listdir(self.boops_directory)))
                    #         self.audio.channel4.play(self.boops[idx])
                    pass
            except IndexError:
                pass
            self.seconds = 0  # Reset timer
        else:
            if self.seconds >= pause:
                return True
        return False
