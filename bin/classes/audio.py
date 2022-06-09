import os

import pygame as pg
from bin.classes.config_manager import Config as c

# Initialize pg.mixer.init() first
# Then pg.mixer.pre_init(48000, -16, 2, 256)
# This ensures any audio playback isn't heavily delayed


class Audio(object):
    def __init__(self):
        # Channels
        self.channel0 = pg.mixer.Channel(0)  # Background Ambience
        self.channel1 = pg.mixer.Channel(1)  # Music
        self.channel2 = pg.mixer.Channel(2)  # Music - Menu Interaction For Music Slider
        self.channel3 = pg.mixer.Channel(3)  # Programmer Voice
        self.channel4 = pg.mixer.Channel(4)  # Glitch Sound Effects
        self.channel5 = pg.mixer.Channel(5)  # Menu Interactions
        self.channel6 = pg.mixer.Channel(6)  # Player Footsteps 1
        self.channel7 = pg.mixer.Channel(7)  # Player Footsteps 1
        self.channel8 = pg.mixer.Channel(8)  # Glitched Exit Error
        self.channel9 = pg.mixer.Channel(9)  # Hit Environment
        self.channel10 = pg.mixer.Channel(10)  # SFX
        self.channel11 = pg.mixer.Channel(11)  # SFX
        self.channel15 = pg.mixer.Channel(15)  # Placeholder
        # Toggles
        self.enable_music = True
        self.enable_sfx = True
        self.change_song = True
        # Config
        # self.config = j.read_json("config.json")  # Read Last Level
        # Volume
        self.vol_music = 100
        self.vol_sfx = 100
        # self.vol_music = self.config.get("music_volume", "")
        # self.vol_sfx = self.config.get("sfx_volume", "")
        # Audio Sets
        self.music_set = []
        self.glitch_set = []
        # Sound Effects

        # Slider Variables
        self.selected_sfx = False
        self.selected_music = False
        self.selected_sfx_o = None
        self.selected_music_o = None
        self.sfx_button_x, self.sfx_button_y = 0, 0  # Default Values
        self.music_button_x, self.music_button_y = 0, 0  # Default Values
        # Other
        self.song = None
        self.channel = 0

    def set_music(self, path, extension):
        """ Loads a specific set of the programmer's dialogue files
        Args:
            path:string:
                Directory to audio files
            extension:string:
                File extension of audio files
        """
        self.music_set = c.load_audio_set(path, extension)

    def load_glitch(self, path, extension):
        """ Loads glitch sound effects into one list
        Args:
            path:string:
                Directory to audio files
            extension:string:
                File extension of audio files
        """
        self.glitch_set = c.load_audio_set(path, extension)

    def song_switch(self, song):
        """ Switch statement to replace if statements - Background ambience manager
        Args:
            song:int:
                Specific song to switch to
        """
        switcher = {
            -1: None,
            0: pg.mixer.Sound(os.getcwd() + "/resources/audio/.mp3"),
            1: pg.mixer.Sound(os.getcwd() + "/resources/audio/.mp3")
        }
        self.song = switcher.get(song, "Invalid Song Request")

    def dj(self, track, channel, fade_channel, ms, change, sfx_c, sfx):
        """ Handles music activation, switching, and fading.
        Args:
            track:int:
                Integer used to fetch a specific song
            channel:int:
                Integer used to specify the channel to play the specific song on
            fade_channel::mixer.channel:
                Specifies a specific Pygame Channel to fade its audio out
            ms:int:
                Specifies how long the fadeout is in milliseconds
            change:bool:
                Changes global boolean to switch songs in play_sounds()
            sfx_c:mixer.channel:
                Specifies a specific Pygame Channel to play a specific sound effect
            sfx:sound file:
                Specifies the sound effect
        Notes:
            This method is built to be called once - E.G. Button Click
        """
        # ------------------------------------------------------------------------------------------------------------------
        if change:
            self.song_switch(track)
            self.channel = channel
            self.change_song = change
        try:
            sfx_c.play(sfx)  # Specified sound effect
            fade_channel.fadeout(ms)
        except AttributeError:
            pass
        # ------------------------------------------------------------------------------------------------------------------

    def play_songs(self):
        """ Switches songs when prompted; based off states, modes, and/or Rick Roll
        Notes:
            pg.mixer.channel.play(Sound, loops=0, maxtime=0, fade_ms=0)
        """
        # ------------------------------------------------------------------------------------------------------------------
        # Music
        try:
            if self.change_song:  # Boolean Activates to Change Song
                pg.mixer.Channel(self.channel).play(self.song, -1)
                self.change_song = False  # Reset Value To Prevent Looping
        except TypeError:
            pass
        # ------------------------------------------------------------------------------------------------------------------

    def set_volume(self):
        """Sets the volume of already declared pygame music mixer channels"""
        # ------------------------------------------------------------------------------------------------------------------
        # Music Channel and Audio Control
        if self.enable_music:
            self.channel0.set_volume(self.vol_music)
            self.channel1.set_volume(self.vol_music)
            self.channel2.set_volume(self.vol_music)
            self.channel0.unpause()
            self.channel1.unpause()
            self.channel2.unpause()
        else:  # Mute Music
            self.channel0.pause()
            self.channel1.pause()
            self.channel2.pause()
            # self.change_song = True  # Reset song choice when un-muted
        # ------------------------------------------------------------------------------------------------------------------
        # Sound Effect Channels & Volume Control
        if self.enable_sfx:
            self.channel3.set_volume(self.vol_sfx)
            self.channel4.set_volume(self.vol_sfx)
            self.channel5.set_volume(self.vol_sfx)
            self.channel6.set_volume(self.vol_sfx)
            self.channel7.set_volume(self.vol_sfx)
            self.channel8.set_volume(self.vol_sfx)
            self.channel9.set_volume(self.vol_sfx)
            self.channel10.set_volume(self.vol_sfx)
            self.channel11.set_volume(self.vol_sfx)
        # Mute Sound Effects - Only pausing doesn't work - music bugs and stops
        else:
            self.channel3.set_volume(0)
            self.channel4.set_volume(0)
            self.channel5.set_volume(0)
            self.channel6.set_volume(0)
            self.channel7.set_volume(0)
            self.channel8.set_volume(0)
            self.channel9.set_volume(0)
            self.channel10.set_volume(0)
            self.channel11.set_volume(0)
        # ------------------------------------------------------------------------------------------------------------------

    def calculate_sfx_volume(self, pos, min_range, normalize):
        """
        Notes:
            Takes in the pos, sets it to a certain range by subtracting min_range. To normalize it to a range of 0-100,
            we divide the number by normalize, giving us a percentage value that we divide again by 100 to get a usable number
            to set the pygame audio channel volume with.

            volume = ((position - minimum range) / normalize) / 100
        """
        self.vol_sfx = ((pos - min_range) / normalize) / 100

    def calculate_music_volume(self, pos, min_range, normalize):
        """
        Notes:
            Takes in the pos, sets it to a certain range by subtracting min_range. To normalize it to a range of 0-100,
            we divide the number by normalize, giving us a percentage value that we divide again by 100 to get a usable number
            to set the pygame audio channel volume with.

            volume = ((position - minimum range) / normalize) / 100
        """
        self.vol_music = ((pos - min_range) / normalize) / 100

    def audio_mixer(self):
        """Parent audio function used to be called in the main loop"""
        self.set_volume()
        self.play_songs()

    @staticmethod
    def fade_out_mixer(time):
        """Static method to fade out all sounds in program.
        Notes:
            @staticmethod lets me identify a function as a Class' method
        """
        pg.mixer.fadeout(time)
