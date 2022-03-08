import math


class Timer(object):
    def __init__(self):
        # Time/Duration
        self.seconds = 0
        self.started_timer = False
        self.activate_timer = False

    def time_start(self):
        """Starts duration timer"""
        self.started_timer, self.activate_timer = True, True

    def time_stop(self):
        """Stops duration timer"""
        if self.activate_timer:
            self.activate_timer = False

    def time_reset(self):
        """Reset duration stopwatch to it's default values"""
        if self.activate_timer:
            self.activate_timer = False
        self.started_timer = False
        self.seconds = 0

    def stopwatch(self):
        """Stopwatch that counts seconds"""
        if self.activate_timer:
            self.seconds += 0.01  # Calculates milliseconds

    def display_stopwatch(self):
        # Rounding the Seconds
        int_seconds = math.floor(self.seconds)

        # Divide by 60 to get total minutes
        minutes = int_seconds // 60

        # Use modulus (remainder) to get seconds
        seconds = int_seconds % 60

        # Use python string formatting to format duration in leading zeros
        output_string = "{0:02}:{1:02}".format(minutes, seconds)
        return output_string
